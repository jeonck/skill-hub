import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// ✏️ 수정 필요: GITHUB_USERNAME, REPO_NAME, SITE_TITLE, SITE_TAGLINE
const GITHUB_USERNAME = 'your-github-username';
const REPO_NAME = 'your-repo-name';
const SITE_TITLE = 'US Work English';
const SITE_TAGLINE = '미국 직장에서 자신 있게 소통하기';

const config: Config = {
  title: SITE_TITLE,
  tagline: SITE_TAGLINE,
  favicon: 'img/favicon.ico',

  future: { v4: true },

  url: `https://${GITHUB_USERNAME}.github.io`,
  baseUrl: `/${REPO_NAME}/`,
  organizationName: GITHUB_USERNAME,
  projectName: REPO_NAME,
  trailingSlash: false,

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'ko',
    locales: ['ko'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: undefined,
        },
        blog: {
          showReadingTime: true,
          feedOptions: { type: ['rss', 'atom'], xslt: true },
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: { customCss: './src/css/custom.css' },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: { respectPrefersColorScheme: true },
    navbar: {
      title: `🇺🇸 ${SITE_TITLE}`,
      items: [
        // ✏️ sidebarId는 sidebars.ts의 키와 일치해야 함
        { type: 'docSidebar', sidebarId: 'jobSearchSidebar',  position: 'left', label: '취업 영어' },
        { type: 'docSidebar', sidebarId: 'workplaceSidebar',  position: 'left', label: '직장 소통' },
        { type: 'docSidebar', sidebarId: 'cultureSidebar',    position: 'left', label: '미국 직장 문화' },
        { type: 'docSidebar', sidebarId: 'phrasebookSidebar', position: 'left', label: '표현 사전' },
        { type: 'docSidebar', sidebarId: 'listeningSidebar',  position: 'left', label: '영어 듣기' },
        { type: 'docSidebar', sidebarId: 'speakingSidebar',   position: 'left', label: '영어 말하기' },
        { to: '/blog', label: '학습 팁', position: 'left' },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Copyright © ${new Date().getFullYear()} ${SITE_TITLE}. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
