/**
 * trustedoss.dev Hero Component
 * CC BY 4.0 · OpenChain KWG · haksungjang
 */

import React from 'react';
import GitHubButton from 'react-github-btn';
import {useColorMode} from '@docusaurus/theme-common';

import styles from './styles.module.css';

function Hero() {
  const {colorMode} = useColorMode();
  return (
    <div className={styles.container}>
      <div className={styles.socialLinks}>
        <GitHubButton
          href="https://github.com/haksungjang/trustedoss"
          data-icon="octicon-star"
          data-size="large"
          data-color-scheme={colorMode}
          aria-label="Star haksungjang/trustedoss on GitHub">
          Star
        </GitHubButton>
      </div>
      <div className={styles.content}>
        <div className={styles.shieldIcon}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 90" width="80" height="90">
            <path d="M40 5 L75 18 L75 48 Q75 72 40 85 Q5 72 5 48 L5 18 Z" fill="#1a7f5a" opacity="0.9"/>
            <path d="M26 44 L35 53 L54 34" stroke="#ffffff" strokeWidth="5" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>
        <h1 className={styles.title}>Trusted OSS</h1>
        <h2 className={styles.subtitle}>신뢰할 수 있는 오픈소스 공급망 관리</h2>
        <p className={styles.description}>
          ISO/IEC 5230 &amp; 18974 기반<br/>
          기업 오픈소스 관리 체계 구축 실전 가이드
        </p>
        <div className={styles.buttonContainer}>
          <a href="/docs" className={styles.primaryButton}>
            체계구축 시작하기
          </a>
          <a href="/ai-coding/intro" className={styles.secondaryButton}>
            AI코딩 가이드
          </a>
        </div>
      </div>
    </div>
  );
}

export default Hero;
