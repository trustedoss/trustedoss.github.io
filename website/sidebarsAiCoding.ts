import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  aiCoding: [
    'intro',
    'strategy',
    'rules-template',
    {
      type: 'category',
      label: '도구별 설정',
      items: [
        'tools/claude-code',
        'tools/cursor',
        'tools/copilot',
        'tools/windsurf',
        'tools/cline-aider',
      ],
    },
    'cicd-quick',
  ],
};

export default sidebars;
