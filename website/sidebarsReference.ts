import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  reference: [
    'intro',
    'glossary',
    {
      type: 'category',
      label: '산출물 Best Practice',
      items: [
        'samples/organization',
        'samples/policy',
        'samples/process',
        'samples/sbom',
        'samples/vulnerability',
        'samples/training',
        'samples/conformance',
      ],
    },
    {
      type: 'category',
      label: '개념 심화',
      items: [
        'concepts/license-classification',
        'concepts/vulnerability-response',
      ],
    },
  ],
};

export default sidebars;
