import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  reference: [
    'intro',
    {
      type: 'category',
      label: '산출물 Best Practice',
      items: [
        'samples/organization',
        'samples/policy',
        'samples/process',
        'samples/training',
        'samples/conformance',
      ],
    },
  ],
};

export default sidebars;
