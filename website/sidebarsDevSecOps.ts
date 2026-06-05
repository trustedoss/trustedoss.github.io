import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  devSecOps: [
    {
      type: 'category',
      label: '시작하기',
      items: ['intro', 'strategy'],
    },
    {
      type: 'category',
      label: '보안 게이트',
      items: [
        'sast',
        'sca',
        'secret-detection',
        'container-security',
        'iac-security',
        'dast',
      ],
    },
    {
      type: 'category',
      label: '파이프라인',
      items: ['pipeline-design', 'monitoring'],
    },
    {
      type: 'category',
      label: '표준 연계',
      items: ['iso-mapping'],
    },
  ],
};

export default sidebars;
