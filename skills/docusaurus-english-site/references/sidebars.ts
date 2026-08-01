import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// ✏️ 섹션을 추가/제거하려면 아래 배열과 docs/ 폴더 구조를 함께 수정
const sidebars: SidebarsConfig = {
  jobSearchSidebar: [
    {
      type: 'category',
      label: '취업 영어',
      collapsed: false,
      items: [
        'job-search/intro',
        'job-search/resume',
        'job-search/cover-letter',
        'job-search/linkedin',
        'job-search/interview',
      ],
    },
  ],

  workplaceSidebar: [
    {
      type: 'category',
      label: '직장 소통',
      collapsed: false,
      items: [
        'workplace/intro',
        'workplace/email',
        'workplace/meetings',
        'workplace/slack-teams',
        'workplace/small-talk',
        'workplace/presentations',
      ],
    },
  ],

  cultureSidebar: [
    {
      type: 'category',
      label: '미국 직장 문화',
      collapsed: false,
      items: [
        'culture/intro',
        'culture/etiquette',
        'culture/feedback',
        'culture/idioms',
      ],
    },
  ],

  phrasebookSidebar: [
    {
      type: 'category',
      label: '표현 사전',
      collapsed: false,
      items: [
        'phrasebook/intro',
        'phrasebook/daily',
        'phrasebook/requests',
        'phrasebook/disagreeing',
      ],
    },
  ],

  listeningSidebar: [
    {
      type: 'category',
      label: '영어 듣기',
      collapsed: false,
      items: [
        'listening/intro',
        'listening/accents',
        'listening/meetings',
        'listening/shadowing',
        'listening/resources',
        'listening/daily',
      ],
    },
  ],

  speakingSidebar: [
    {
      type: 'category',
      label: '영어 말하기',
      collapsed: false,
      items: [
        'speaking/intro',
        'speaking/pronunciation',
        'speaking/fluency',
        'speaking/fillers',
        'speaking/practice',
        'speaking/daily',
      ],
    },
  ],
};

export default sidebars;
