#!/usr/bin/env bash
# Enable GitHub Pages (Actions build) on a repo, and optionally attach + enforce
# HTTPS on a custom domain. Requires `gh` authenticated with repo admin rights.
#
# Usage:
#   ./setup_github_pages.sh <owner>/<repo> [custom-domain]
#
# Examples:
#   ./setup_github_pages.sh jeonck/cybersecurity
#   ./setup_github_pages.sh jeonck/cybersecurity docs.example.com
#
# What this does, and why each step exists:
#   1. POST /repos/{owner}/{repo}/pages with build_type=workflow
#      -> tells GitHub Pages to deploy from a GitHub Actions artifact instead
#         of a branch. Required for a Hugo Modules site (or any build step).
#   2. If a domain is given: PUT .../pages with cname=<domain>
#      -> attaches the custom domain. Also (re)write static/CNAME in the repo
#         so Hugo copies it into `public/` on every build — GitHub Pages
#         resets the custom domain if the CNAME file goes missing from a
#         deploy, and Hugo Modules sites often gitignore `public/`, so the
#         CNAME must live in `static/` to survive the build.
#   3. Poll until the HTTPS certificate state is "approved" (DNS must already
#      point at GitHub Pages — this script does not configure DNS).
#   4. PUT .../pages with https_enforced=true
#      -> NOTE: `gh api -f https_enforced=true` sends the STRING "true" and
#         GitHub rejects it (422: not of type boolean). Must use `-F`
#         (capital), which sends a real JSON boolean. This is the single
#         most common way this step silently fails.
set -euo pipefail

REPO="${1:?usage: setup_github_pages.sh <owner>/<repo> [custom-domain]}"
DOMAIN="${2:-}"

echo "==> Enabling GitHub Pages (Actions build) on $REPO"
gh api -X POST "repos/$REPO/pages" -f build_type=workflow >/dev/null 2>&1 || \
  echo "    (already enabled, continuing)"

if [[ -n "$DOMAIN" ]]; then
  echo "==> Attaching custom domain: $DOMAIN"
  gh api -X PUT "repos/$REPO/pages" -f cname="$DOMAIN" >/dev/null

  echo "==> Checking DNS resolves to GitHub Pages"
  if ! dig +short "$DOMAIN" | grep -qE '185\.199\.10[89]\.153|185\.199\.11[01]\.153|github\.io\.$'; then
    echo "    WARNING: $DOMAIN does not appear to resolve to GitHub Pages yet."
    echo "    Point it at a CNAME to <owner>.github.io (or the four GitHub Pages"
    echo "    A records: 185.199.108/109/110/111.153), then re-run this script."
  fi

  echo "==> Waiting for GitHub to issue/approve the HTTPS certificate..."
  for _ in $(seq 1 20); do
    STATE=$(gh api "repos/$REPO/pages" --jq '.https_certificate.state // "pending"')
    echo "    cert state: $STATE"
    [[ "$STATE" == "approved" ]] && break
    sleep 15
  done

  if [[ "$STATE" == "approved" ]]; then
    echo "==> Enforcing HTTPS (note: -F, not -f, for a real boolean)"
    gh api -X PUT "repos/$REPO/pages" -F https_enforced=true >/dev/null
  else
    echo "    Certificate not approved yet after waiting; skipping https_enforced."
    echo "    Re-run this script once DNS has propagated: ./setup_github_pages.sh $REPO $DOMAIN"
  fi
fi

echo "==> Final Pages status:"
gh api "repos/$REPO/pages" --jq '{cname, https_enforced, html_url, cert_state: .https_certificate.state}'
