/**
 * trustedoss.github.io Hero — Vercel풍 (고대비 모노크롬, 큰 타이포, 미세 그리드)
 * CC BY 4.0 · OpenChain KWG · haksungjang
 */

import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import Translate, {translate} from '@docusaurus/Translate';

import styles from './styles.module.css';

function Hero() {
  const meta = [
    'ISO/IEC 5230',
    'ISO/IEC 18974',
    'CC BY 4.0',
    translate({id: 'homepage.hero.meta.vendorNeutral', message: '벤더중립'}),
  ];
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
          <Link
            className="button button--primary button--lg"
            to="/docs/overview/quick-start">
            {translate({
              id: 'homepage.hero.cta.quickstart',
              message: '처음이세요? 5분 빠른 시작',
            })}
          </Link>
          <Link className="button button--secondary button--lg" to="/docs">
            {translate({
              id: 'homepage.hero.cta.start',
              message: '전체 가이드 보기',
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
        <div className={styles.visual} aria-hidden="true">
          <div className={styles.window}>
            <div className={styles.windowBar}>
              <i />
              <i />
              <i />
              <span className={styles.windowTitle}>
                agents/02-organization-designer
              </span>
            </div>
            <div className={styles.windowBody}>
              <p className={styles.cmd}>
                <span className={styles.prompt}>$</span> claude
              </p>
              <p className={styles.muted}>
                <Translate id="homepage.hero.terminal.progress">
                  회사 상황 6개 질문에 답하는 중…
                </Translate>
              </p>
              <p className={styles.gen}>
                <span className={styles.check}>✓</span> role-definition.md
              </p>
              <p className={styles.gen}>
                <span className={styles.check}>✓</span> raci-matrix.md
              </p>
              <div className={styles.chips}>
                <span>
                  <Translate id="homepage.hero.terminal.chip.policy">
                    정책
                  </Translate>
                </span>
                <span>SBOM</span>
                <span>
                  <Translate id="homepage.hero.terminal.chip.vulnerability">
                    취약점
                  </Translate>
                </span>
                <span>
                  <Translate id="homepage.hero.terminal.chip.declaration">
                    선언문
                  </Translate>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Hero;
