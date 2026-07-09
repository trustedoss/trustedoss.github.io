import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  aiCoding: [
    {
      type: 'category',
      label: '시작하기',
      items: ['intro', 'strategy', 'rules-template'],
    },
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
    {
      type: 'category',
      label: '실전 적용',
      items: [
        'cicd-quick',
        'ai-security-review',
        'legal-considerations',
        'iso42001',
        'best-practice-repo',
      ],
    },
    {
      type: 'category',
      label: '표준 연계',
      items: ['iso-mapping'],
    },
  ],
};

export default sidebars;
