/**
 * trustedoss.dev Homepage
 * CC BY 4.0 · OpenChain KWG · haksungjang
 */

import React from 'react';

import Head from '@docusaurus/Head';
import {translate} from '@docusaurus/Translate';
import Layout from '@theme/Layout';

import Home from '../components/Home';

const Index = () => {
  return (
    <Layout
      description={translate({
        id: 'homepage.meta.description',
        message:
          'ISO/IEC 5230 & 18974 기반 기업 오픈소스 관리 체계 구축 실전 가이드',
      })}
      wrapperClassName="homepage">
      <Head>
        <title>
          {translate({
            id: 'homepage.meta.title',
            message: 'Trusted OSS · 신뢰할 수 있는 오픈소스 공급망 관리',
          })}
        </title>
        <meta
          property="og:title"
          content={translate({
            id: 'homepage.meta.title',
            message: 'Trusted OSS · 신뢰할 수 있는 오픈소스 공급망 관리',
          })}
        />
        <meta
          property="twitter:title"
          content={translate({
            id: 'homepage.meta.title',
            message: 'Trusted OSS · 신뢰할 수 있는 오픈소스 공급망 관리',
          })}
        />
      </Head>
      <Home />
    </Layout>
  );
};

export default Index;
