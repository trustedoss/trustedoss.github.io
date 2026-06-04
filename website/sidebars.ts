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
      type: 'doc',
      id: 'setup/index',
      label: '1. 환경 준비 (30분)',
    },
    {
      type: 'doc',
      id: 'organization/index',
      label: '2. 조직 구성 (1시간)',
    },
    {
      type: 'doc',
      id: 'policy/index',
      label: '3. 오픈소스 정책 (1시간)',
    },
    {
      type: 'doc',
      id: 'process/index',
      label: '4. 오픈소스 프로세스 (1시간)',
    },
    {
      type: 'category',
      label: '5. 도구 (약 3시간)',
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
      type: 'doc',
      id: 'training/index',
      label: '6. 교육 체계 (30분)',
    },
    {
      type: 'doc',
      id: 'conformance/index',
      label: '7. 자체 인증 (30분)',
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
