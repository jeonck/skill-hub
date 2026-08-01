#!/usr/bin/env bash
# Copy the Remotion explainer scaffold into a target dir and install deps.
# Usage: scaffold_project.sh <target-dir> [--audio]
#   --audio also copies the SFX + BGM bundled with the video-shotcraft skill
#           (free commercial-use) into <target>/public/audio if that skill exists.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCAFFOLD="$HERE/assets/scaffold"
TARGET="${1:?usage: scaffold_project.sh <target-dir> [--audio]}"
WANT_AUDIO="${2:-}"

mkdir -p "$TARGET"
# copy everything except any stray node_modules symlink
rsync -a --exclude node_modules "$SCAFFOLD"/ "$TARGET"/
mkdir -p "$TARGET/public/audio" "$TARGET/out/qa"

if [ "$WANT_AUDIO" = "--audio" ]; then
  AUDIO_SRC="$HOME/.agents/skills/video-shotcraft/assets/audio"
  if [ -d "$AUDIO_SRC" ]; then
    for f in keyboard whoosh-fast whoosh-big swoosh-quick transition-soft transition-snap \
             impact-cine impact-deep-whoosh riser-cine sparkle shimmer-sparkle-sweep pop \
             sub-bass-knock drum-impact-subtle tick-percussion; do
      cp "$AUDIO_SRC/$f.mp3" "$TARGET/public/audio/" 2>/dev/null || true
    done
    cp "$AUDIO_SRC/bgm/bgm-tech-house.mp3" "$TARGET/public/audio/bgm.mp3" 2>/dev/null || true
    echo "copied audio into $TARGET/public/audio"
  else
    echo "note: video-shotcraft audio not found at $AUDIO_SRC — add your own SFX/BGM"
  fi
fi

echo "installing deps in $TARGET ..."
( cd "$TARGET" && npm install >/dev/null 2>&1 ) && echo "npm install done" || echo "npm install failed — run it manually"

echo "scaffold ready. Try:  cd $TARGET && npx remotion still src/index.ts Explainer out/qa/f130.png --frame=130"
