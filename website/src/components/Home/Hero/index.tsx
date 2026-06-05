/**
 * trustedoss.dev Hero — Vercel풍 (고대비 모노크롬, 큰 타이포, 미세 그리드)
 * CC BY 4.0 · OpenChain KWG · haksungjang
 */

import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import Translate, {translate} from '@docusaurus/Translate';

import styles from './styles.module.css';

const meta = ['ISO/IEC 5230', 'ISO/IEC 18974', 'CC BY 4.0', '벤더중립'];

function Hero() {
  return (
    <header className={styles.hero}>
      <div className={clsx('container', styles.container)}>
        <p className={styles.eyebrow}>
          <span className={styles.dot} aria-hidden="true" />
          <Translate id="homepage.hero.eyebrow">
            OpenChain KWG · 무료 셀프스터디 가이드
          </Translate>
        </p>
        <h1 className={styles.title}>
          <Translate id="homepage.hero.title.line1">오픈소스 신뢰를,</Translate>
          <br />
          <span className={styles.titleAccent}>
            <Translate id="homepage.hero.title.line2">
              스스로 세웁니다.
            </Translate>
          </span>
        </h1>
        <p className={styles.subtitle}>
          <Translate id="homepage.hero.subtitle.content">
            ISO/IEC 5230 & 18974 기반 오픈소스 관리 체계를 벤더 컨설팅 없이
            단계별로 구축하고, 자체 인증 선언까지 도달합니다.
          </Translate>
        </p>
        <div className={styles.ctas}>
          <Link className="button button--primary button--lg" to="/docs">
            {translate({
              id: 'homepage.hero.cta.start',
              message: '가이드 시작하기',
            })}
          </Link>
          <Link
            className="button button--secondary button--lg"
            href="https://github.com/trustedoss/trustedoss.github.io">
            <span className={styles.ghIcon} aria-hidden="true" />
            GitHub
          </Link>
        </div>
        <ul className={styles.meta}>
          {meta.map(item => (
            <li key={item} className={styles.metaItem}>
              {item}
            </li>
          ))}
        </ul>
      </div>
    </header>
  );
}

export default Hero;
