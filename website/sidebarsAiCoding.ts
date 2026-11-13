import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  aiCoding: [
    {
      type: 'category',
      label: '시작하기',
      items: ['intro'],
    },
    {
      type: 'category',
      label: '거버넌스 기반',
      items: ['usage-policy', 'legal-considerations', 'iso42001'],
    },
    {
      type: 'category',
      label: '보안·컴플라이언스 통제',
      items: [
        'strategy',
        'rules-template',
        'cicd-quick',
        'ai-security-review',
        'ai-fuzzing',
        'agent-governance',
      ],
    },
    {
      type: 'category',
      label: '협업과 테스트',
      items: ['collaboration', 'testing'],
    },
    {
      type: 'category',
      label: '도구별 설정',
      items: [
        'tools/claude-code',
        'tools/copilot',
        'tools/codex',
        'tools/cursor',
        'tools/windsurf',
        'tools/cline-aider',
      ],
    },
    {
      type: 'category',
      label: '참조 구현과 표준 연계',
      items: [
        'best-practice-repo',
        {type: 'doc', id: 'iso-mapping', label: '표준 대응: AI 코딩'},
      ],
    },
  ],
};

export default sidebars;
