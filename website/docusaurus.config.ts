/**
 * trustedoss.dev - Trusted OSS Supply Chain Management Guide
 * CC BY 4.0 · OpenChain KWG · haksungjang
 */

import type * as PluginContentDocs from '@docusaurus/plugin-content-docs';
import type * as Preset from '@docusaurus/preset-classic';
import type {Config} from '@docusaurus/types';

import prismTheme from './core/PrismTheme';

// See https://docs.netlify.com/configure-builds/environment-variables/
const isProductionDeployment =
  !!process.env.NETLIFY && process.env.CONTEXT === 'production';

const copyright = `CC BY 4.0 · OpenChain KWG · haksungjang`;

const config: Config = {
  future: {
    v4: true,
    experimental_faster: (process.env.DOCUSAURUS_FASTER ?? 'true') === 'true',
  },

  title: 'Trusted OSS',
  tagline: '신뢰할 수 있는 오픈소스 공급망 관리',
  organizationName: 'trustedoss',
  projectName: 'trustedoss.github.io',
  url: 'https://trustedoss.github.io/',
  baseUrl: '/',
  clientModules: ['./modules/jumpToFragment.ts'],
  trailingSlash: false,
  scripts: [
    {
      src: 'https://cdn.jsdelivr.net/npm/focus-visible@5.2.0/dist/focus-visible.min.js',
      defer: true,
    },
  ],
  favicon: 'img/favicon.svg',
  titleDelimiter: '·',
  i18n: {
    defaultLocale: 'ko',
    locales: ['ko'],
  },
  onBrokenLinks: 'warn',
  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],
  headTags: [
    {
      tagName: 'script',
      attributes: {
        type: 'application/ld+json',
      },
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org/',
        '@type': 'WebSite',
        '@id': 'https://trustedoss.github.io/',
        url: 'https://trustedoss.github.io/',
        name: 'Trusted OSS · 신뢰할 수 있는 오픈소스 공급망 관리',
        description:
          'ISO/IEC 5230 & 18974 기반 기업 오픈소스 관리 체계 구축 실전 가이드',
        inLanguage: 'ko',
      }),
    },
  ],
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          path: '../docs',
          sidebarPath: require.resolve('./sidebars'),
          breadcrumbs: false,
          showLastUpdateAuthor: false,
          showLastUpdateTime: false,
          editUrl:
            'https://github.com/trustedoss/trustedoss.github.io/edit/main/',
        },
        blog: {
          path: 'blog',
          blogSidebarCount: 'ALL',
          blogSidebarTitle: '전체 블로그 포스트',
          feedOptions: {
            type: 'all',
            copyright,
          },
          onInlineAuthors: 'ignore',
          onUntruncatedBlogPosts: 'ignore',
        },
        theme: {
          customCss: [
            require.resolve('./src/css/customTheme.scss'),
            require.resolve('./src/css/index.scss'),
          ],
        },
        gtag: {
          trackingID: 'G-TRUSTEDOSS01',
        },
      } satisfies Preset.Options,
    ],
  ],
  plugins: [
    'docusaurus-plugin-sass',
    function disableExpensiveBundlerOptimizationPlugin() {
      return {
        name: 'disable-expensive-bundler-optimizations',
        configureWebpack(_config: unknown, isServer: boolean) {
          return {
            optimization: {
              concatenateModules: isProductionDeployment ? !isServer : false,
            },
          };
        },
      };
    },
    [
      'content-docs',
      {
        id: 'ai-coding',
        path: 'ai-coding',
        routeBasePath: '/ai-coding',
        sidebarPath: require.resolve('./sidebarsAiCoding'),
        breadcrumbs: false,
        showLastUpdateAuthor: false,
        showLastUpdateTime: false,
      } satisfies PluginContentDocs.Options,
    ],
    [
      'content-docs',
      {
        id: 'devsecops',
        path: 'devsecops',
        routeBasePath: 'devsecops',
        sidebarPath: require.resolve('./sidebarsDevSecOps'),
        breadcrumbs: false,
        showLastUpdateAuthor: false,
        showLastUpdateTime: false,
      } satisfies PluginContentDocs.Options,
    ],
    [
      'content-docs',
      {
        id: 'reference',
        path: 'reference',
        routeBasePath: 'reference',
        sidebarPath: require.resolve('./sidebarsReference'),
        breadcrumbs: false,
        showLastUpdateAuthor: false,
        showLastUpdateTime: false,
      } satisfies PluginContentDocs.Options,
    ],
  ],
  themeConfig: {
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    prism: {
      defaultLanguage: 'bash',
      theme: prismTheme,
      additionalLanguages: [
        'diff',
        'bash',
        'json',
        'yaml',
        'java',
        'kotlin',
        'groovy',
      ],
      magicComments: [
        {
          className: 'theme-code-block-highlighted-line',
          line: 'highlight-next-line',
          block: {start: 'highlight-start', end: 'highlight-end'},
        },
        {
          className: 'code-add-line',
          line: 'highlight-add-next-line',
          block: {start: 'highlight-add-start', end: 'highlight-add-end'},
        },
        {
          className: 'code-remove-line',
          line: 'highlight-remove-next-line',
          block: {
            start: 'highlight-remove-start',
            end: 'highlight-remove-end',
          },
        },
      ],
    },
    navbar: {
      title: 'Trusted OSS',
      logo: {
        src: 'img/header_logo.svg',
        alt: 'Trusted OSS Logo',
      },
      style: 'dark',
      items: [
        {
          to: '/docs',
          label: '체계구축',
          position: 'left',
        },
        {
          to: '/devsecops/intro',
          label: 'DevSecOps',
          position: 'left',
        },
        {
          to: '/ai-coding/intro',
          label: 'AI코딩',
          position: 'left',
        },
        {
          to: '/reference/intro',
          label: '레퍼런스',
          position: 'left',
        },
        {
          href: 'https://github.com/haksungjang/trustedoss',
          'aria-label': 'GitHub repository',
          position: 'right',
          className: 'navbar-github-link',
        },
      ],
    },
    image: 'img/logo-share.png',
    footer: {
      style: 'dark',
      links: [
        {
          title: '가이드',
          items: [
            {
              label: '체계구축',
              to: '/docs',
            },
            {
              label: 'DevSecOps',
              to: '/devsecops/intro',
            },
            {
              label: 'AI코딩',
              to: '/ai-coding/intro',
            },
            {
              label: '레퍼런스',
              to: '/reference/intro',
            },
            {
              label: '블로그',
              to: '/blog',
            },
          ],
        },
        {
          title: '커뮤니티',
          items: [
            {
              label: 'OpenChain KWG',
              href: 'https://openchain-project.github.io/OpenChain-KWG/',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/haksungjang/trustedoss',
            },
          ],
        },
        {
          title: '표준',
          items: [
            {
              label: 'ISO/IEC 5230',
              href: 'https://www.iso.org/standard/81039.html',
            },
            {
              label: 'ISO/IEC 18974',
              href: 'https://www.iso.org/standard/86450.html',
            },
            {
              label: 'OpenChain 자체 인증',
              href: 'https://www.openchainproject.org/conformance',
            },
          ],
        },
      ],
      copyright,
    },
    metadata: [
      {
        property: 'og:image',
        content: 'https://trustedoss.dev/img/logo-share.png',
      },
      {name: 'twitter:card', content: 'summary_large_image'},
      {
        name: 'twitter:image',
        content: 'https://trustedoss.dev/img/logo-share.png',
      },
      {name: 'mobile-web-app-capable', content: 'yes'},
    ],
  } satisfies Preset.ThemeConfig,
};

export default config;
