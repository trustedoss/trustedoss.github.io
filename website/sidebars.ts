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
      label: '0. 시작하기',
      collapsed: false,
      items: [
        'overview/index',
        'overview/checklist-mapping',
        {
          type: 'category',
          label: '소프트웨어 공급망 보안',
          items: [
            '00b-supply-chain/index',
            '00b-supply-chain/sbom-101',
          ],
        },
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
      label: '5. 도구',
      collapsed: false,
      items: [
        'tools/sbom-generation/index',
        'tools/sbom-management/index',
        'tools/vulnerability/index',
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
      label: '7. 자체 인증 선언',
    },
    {
      type: 'doc',
      id: 'developer-guide/08-developer-guide',
      label: '8. 개발자 가이드',
    },
  ],
};

export default sidebars;
