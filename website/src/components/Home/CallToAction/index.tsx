/**
 * trustedoss.dev CallToAction Component
 * CC BY 4.0 · OpenChain KWG · haksungjang
 */

import React from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';

import styles from './styles.module.css';

const features = [
  {
    icon: '🏗️',
    title: '체계구축',
    description: 'ISO/IEC 5230 & 18974 기반으로 기업 오픈소스 관리 체계를 처음부터 완성까지 구축합니다.',
    link: '/docs',
    linkLabel: '가이드 시작하기',
  },
  {
    icon: '🔒',
    title: 'DevSecOps',
    description: '개발 파이프라인에 보안을 통합합니다. SAST, SCA, 컨테이너 보안, CI/CD 자동화를 다룹니다.',
    link: '/devsecops/intro',
    linkLabel: 'DevSecOps 가이드',
  },
  {
    icon: '🤖',
    title: 'AI코딩',
    description: 'Claude Code, Cursor, Copilot 등 AI 코딩 도구와 오픈소스 컴플라이언스를 함께 관리합니다.',
    link: '/ai-coding/intro',
    linkLabel: 'AI코딩 가이드',
  },
];

function FeatureCard({icon, title, description, link, linkLabel}: (typeof features)[0]) {
  const url = useBaseUrl(link);
  return (
    <div className={styles.featureCard}>
      <div className={styles.featureIcon}>{icon}</div>
      <h3 className={styles.featureTitle}>{title}</h3>
      <p className={styles.featureDescription}>{description}</p>
      <a href={url} className={styles.featureLink}>
        {linkLabel} →
      </a>
    </div>
  );
}

function CallToAction() {
  const docsUrl = useBaseUrl('/docs');
  return (
    <div className={styles.wrapper}>
      <div className={styles.featuresGrid}>
        {features.map(feature => (
          <FeatureCard key={feature.title} {...feature} />
        ))}
      </div>
      <div className={styles.container}>
        <h2 className={styles.title}>오픈소스 관리, 지금 시작하세요</h2>
        <p className={styles.subtitle}>
          OpenChain KWG 커뮤니티가 제공하는 무료 가이드로<br/>
          ISO/IEC 5230 & 18974 자체 인증 선언까지 완성하세요.
        </p>
        <a href={docsUrl} className={styles.primaryButton}>
          체계구축 시작하기
        </a>
      </div>
    </div>
  );
}

export default CallToAction;
