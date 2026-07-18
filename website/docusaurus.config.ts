/**
 * trustedoss.github.io - Trusted OSS Supply Chain Management Guide
 * CC BY 4.0 · OpenChain KWG · haksungjang
 */

import type * as PluginContentDocs from '@docusaurus/plugin-content-docs';
import type * as Preset from '@docusaurus/preset-classic';
import type {Config} from '@docusaurus/types';

import {themes as prismThemes} from 'prism-react-renderer';

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
  clientModules: ['./modules/jumpToFragment.ts', './modules/fonts.ts'],
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
    locales: ['ko', 'en'], // 'en' 추가
    localeConfigs: {
      ko: {label: '한국어'},
      en: {label: 'English'},
    },
  },
  onBrokenLinks: 'throw',
  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'throw',
    },
  },
  themes: [
    '@docusaurus/theme-mermaid',
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      {
        hashed: true,
        language: ['ko', 'en'],
        indexDocs: true,
        indexBlog: true,
        indexPages: false,
        // 체계구축(docs) 외 별도 content-docs 인스턴스도 검색에 포함
        docsRouteBasePath: ['/docs', '/devsecops', '/ai-coding', '/reference'],
        highlightSearchTermsOnTargetPage: true,
        searchResultLimits: 8,
        searchResultContextMaxLength: 50,
      },
    ],
  ],
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
          // 내부 지침 파일은 독자 비노출 (빌드·검색 인덱스 제외)
          // exclude를 지정하면 기본 제외 목록이 덮어써지므로 기본값(_* 등)도 함께 나열한다
          exclude: [
            '**/_*.{js,jsx,ts,tsx,md,mdx}',
            '**/_*/**',
            '**/*.test.{js,jsx,ts,tsx}',
            '**/__tests__/**',
            '**/CLAUDE.md',
          ],
          sidebarPath: require.resolve('./sidebars'),
          breadcrumbs: true,
          showLastUpdateAuthor: false,
          showLastUpdateTime: false,
          // docs가 website 밖(../docs)에 있어 문자열 형식이면 '../docs'가 URL에 섞여 404가 된다
          editUrl: ({docPath}) =>
            `https://github.com/trustedoss/trustedoss.github.io/edit/main/docs/${docPath}`,
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
        breadcrumbs: true,
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
        breadcrumbs: true,
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
        breadcrumbs: true,
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
    mermaid: {
      options: {
        fontSize: 18,
        themeVariables: {
          fontSize: '18px',
        },
        flowchart: {
          padding: 12,
          nodeSpacing: 30,
          rankSpacing: 30,
        },
      },
    },
    prism: {
      defaultLanguage: 'bash',
      theme: prismThemes.github,
      darkTheme: prismThemes.vsDark,
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
      items: [
        {
          to: '/docs',
          label: '오픈소스 관리',
          position: 'left',
        },
        {
          to: '/devsecops/intro',
          label: 'DevSecOps',
          position: 'left',
        },
        {
          to: '/ai-coding/intro',
          label: 'AI 코딩 거버넌스',
          position: 'left',
        },
        {
          to: '/reference/intro',
          label: '레퍼런스',
          position: 'left',
        },
        // {
        //   to: '/blog',
        //   label: '블로그',
        //   position: 'left',
        // },
        {
          href: 'https://trustedoss.github.io/trusca/',
          label: 'TRUSCA',
          position: 'right',
        },
        {
          type: 'localeDropdown',
          position: 'right',
        },
        {
          href: 'https://github.com/trustedoss',
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
              label: '오픈소스 관리',
              to: '/docs',
            },
            {
              label: 'DevSecOps',
              to: '/devsecops/intro',
            },
            {
              label: 'AI 코딩 거버넌스',
              to: '/ai-coding/intro',
            },
            {
              label: '레퍼런스',
              to: '/reference/intro',
            },
            {
              label: 'TRUSCA',
              href: 'https://trustedoss.github.io/trusca/',
            },
            // {
            //   label: '블로그',
            //   to: '/blog',
            // },
          ],
        },
        {
          title: '커뮤니티',
          items: [
            {
              label: '이 프로젝트에 대하여',
              to: '/about',
            },
            {
              label: 'OpenChain KWG',
              href: 'https://openchain-project.github.io/OpenChain-KWG/',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/trustedoss',
            },
            {
              label: '기여 가이드',
              href: 'https://github.com/trustedoss/trustedoss.github.io/blob/main/CONTRIBUTING.md',
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
        content: 'https://trustedoss.github.io/img/logo-share.png',
      },
      {name: 'twitter:card', content: 'summary_large_image'},
      {
        name: 'twitter:image',
        content: 'https://trustedoss.github.io/img/logo-share.png',
      },
      {name: 'mobile-web-app-capable', content: 'yes'},
    ],
  } satisfies Preset.ThemeConfig,
};

export default config;
