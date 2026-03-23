import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docs: [
    {
      type: 'category',
      label: '시작하기',
      collapsed: false,
      items: [
        'overview/index',
        'overview/checklist-mapping',
        'overview/supply-chain',
        'overview/sbom-101',
      ],
    },
    {
      type: 'category',
      label: '환경 준비',
      collapsed: false,
      items: [
        'setup/index',
      ],
    },
    {
      type: 'category',
      label: '조직 구성',
      collapsed: false,
      items: [
        'organization/index',
      ],
    },
    {
      type: 'category',
      label: '오픈소스 정책',
      collapsed: false,
      items: [
        'policy/index',
      ],
    },
    {
      type: 'category',
      label: '오픈소스 프로세스',
      collapsed: false,
      items: [
        'process/index',
      ],
    },
    {
      type: 'category',
      label: '도구',
      collapsed: false,
      items: [
        'tools/sbom-generation/index',
        'tools/sbom-generation/docker-cicd',
        'tools/sbom-management/index',
        'tools/vulnerability/index',
        'tools/vulnerability/tools-setup',
      ],
    },
    {
      type: 'category',
      label: '교육 체계',
      collapsed: false,
      items: [
        'training/index',
      ],
    },
    {
      type: 'category',
      label: '자체 인증',
      collapsed: false,
      items: [
        'conformance/index',
      ],
    },
    {
      type: 'category',
      label: '개발자 가이드 (선택)',
      collapsed: false,
      items: [
        'developer-guide/08-developer-guide',
        'developer-guide/method1-claude-md',
        'developer-guide/method2-skill',
        'developer-guide/method3-hooks',
        'developer-guide/method4-cicd',
      ],
    },
  ],
};

export default sidebars;
