/**
 * Prism 구문 강조 테마 — Gemini docs 스타일.
 * 라이트(기본)와 다크를 분리해 라이트 모드에서 라이트 코드가 나오게 한다.
 */

import type {ThemeConfig} from '@docusaurus/preset-classic';

type PrismTheme = ThemeConfig['prism']['theme'];

/** 라이트 코드 테마 (Gemini docs 톤: 밝은 배경 + 차분한 구문색) */
export const lightTheme: PrismTheme = {
  plain: {
    color: '#383a42',
    backgroundColor: '#f8f9fa',
  },
  styles: [
    {
      types: ['comment', 'prolog', 'doctype', 'cdata'],
      style: {color: '#5f6368', fontStyle: 'italic'},
    },
    {types: ['punctuation'], style: {color: '#383a42'}},
    {types: ['namespace'], style: {opacity: 0.7}},
    {
      types: ['keyword', 'atrule', 'selector'],
      style: {color: '#8430ce'},
    },
    {
      types: ['string', 'char', 'attr-value', 'inserted'],
      style: {color: '#188038'},
    },
    {
      types: ['number', 'boolean', 'constant', 'symbol', 'deleted'],
      style: {color: '#c5221f'},
    },
    {
      types: ['function', 'class-name', 'builtin'],
      style: {color: '#1a73e8'},
    },
    {types: ['variable', 'attr-name'], style: {color: '#b06000'}},
    {types: ['operator', 'tag'], style: {color: '#383a42'}},
    {types: ['url', 'entity'], style: {color: '#1a73e8'}},
    {types: ['important', 'bold'], style: {fontWeight: 'bold'}},
    {types: ['italic'], style: {fontStyle: 'italic'}},
  ],
};

/** 다크 코드 테마 (다크 모드용) */
export const darkTheme: PrismTheme = {
  plain: {
    color: '#e3e3e3',
    backgroundColor: '#1f1f1f',
  },
  styles: [
    {
      types: ['comment', 'prolog', 'doctype', 'cdata'],
      style: {color: '#9aa0a6', fontStyle: 'italic'},
    },
    {types: ['punctuation'], style: {color: '#e3e3e3'}},
    {types: ['namespace'], style: {opacity: 0.7}},
    {
      types: ['keyword', 'atrule', 'selector'],
      style: {color: '#c58af9'},
    },
    {
      types: ['string', 'char', 'attr-value', 'inserted'],
      style: {color: '#7ee787'},
    },
    {
      types: ['number', 'boolean', 'constant', 'symbol', 'deleted'],
      style: {color: '#ff8a80'},
    },
    {
      types: ['function', 'class-name', 'builtin'],
      style: {color: '#8ab4f8'},
    },
    {types: ['variable', 'attr-name'], style: {color: '#fdd663'}},
    {types: ['operator', 'tag'], style: {color: '#e3e3e3'}},
    {types: ['url', 'entity'], style: {color: '#8ab4f8'}},
    {types: ['important', 'bold'], style: {fontWeight: 'bold'}},
    {types: ['italic'], style: {fontStyle: 'italic'}},
  ],
};

export default lightTheme;
