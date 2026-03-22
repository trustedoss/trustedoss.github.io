import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docs: [
    {
      type: 'doc',
      id: 'intro',
      label: '소개',
    },
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
      type: 'doc',
      id: 'setup/index',
      label: '환경 준비',
    },
    {
      type: 'doc',
      id: 'organization/index',
      label: '조직 구성',
    },
    {
      type: 'doc',
      id: 'policy/index',
      label: '오픈소스 정책',
    },
    {
      type: 'doc',
      id: 'process/index',
      label: '오픈소스 프로세스',
    },
    {
      type: 'category',
      label: '도구',
      collapsed: false,
      items: [
        {
          type: 'category',
          label: 'SBOM 생성',
          items: [
            'tools/sbom-generation/index',
            'tools/sbom-generation/docker-cicd',
          ],
        },
        {
          type: 'doc',
          id: 'tools/sbom-management/index',
          label: 'SBOM 관리',
        },
        {
          type: 'category',
          label: '취약점 분석',
          items: [
            'tools/vulnerability/index',
            'tools/vulnerability/tools-setup',
          ],
        },
      ],
    },
    {
      type: 'doc',
      id: 'training/index',
      label: '교육 체계',
    },
    {
      type: 'doc',
      id: 'conformance/index',
      label: '자체 인증',
    },
    {
      type: 'category',
      label: '개발자 가이드 (선택)',
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
