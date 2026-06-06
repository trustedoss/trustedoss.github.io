import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docs: [
    {
      type: 'category',
      label: '시작하기',
      collapsed: true,
      items: [
        'overview/quick-start',
        'overview/start-path',
        'overview/index',
        'overview/agents',
      ],
    },
    {
      type: 'category',
      label: '배경 지식',
      collapsed: true,
      items: [
        'overview/supply-chain',
        'overview/sbom-101',
        'overview/checklist-mapping',
      ],
    },
    {
      type: 'doc',
      id: 'setup/index',
      label: '1. 환경 준비',
    },
    {
      type: 'doc',
      id: 'organization/index',
      label: '2. 조직 구성',
    },
    {
      type: 'doc',
      id: 'policy/index',
      label: '3. 오픈소스 정책',
    },
    {
      type: 'doc',
      id: 'process/index',
      label: '4. 오픈소스 프로세스',
    },
    {
      type: 'category',
      label: '5. 도구: SBOM과 취약점',
      collapsed: true,
      link: {type: 'doc', id: 'tools/index'},
      items: [
        'tools/sbom-generation/index',
        'tools/sbom-generation/docker-cicd',
        'tools/sbom-management/index',
        'tools/vulnerability/index',
        'tools/vulnerability/tools-setup',
      ],
    },
    {
      type: 'doc',
      id: 'training/index',
      label: '6. 교육 체계',
    },
    {
      type: 'doc',
      id: 'conformance/index',
      label: '7. 자체 인증',
    },
    {
      type: 'category',
      label: '개발자 가이드 (선택)',
      collapsed: true,
      link: {type: 'doc', id: 'developer-guide/08-developer-guide'},
      items: [
        'developer-guide/method1-claude-md',
        'developer-guide/method2-skill',
        'developer-guide/method3-hooks',
        'developer-guide/method4-cicd',
      ],
    },
  ],
};

export default sidebars;
