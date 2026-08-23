/**
 * trustedoss.github.io FinalCTA — 클로징 밴드 (Vercel풍 고대비)
 * CC BY 4.0 · TrustedOSS Contributors
 */

import React from 'react';
import Link from '@docusaurus/Link';
import Translate, {translate} from '@docusaurus/Translate';

import styles from './styles.module.css';

function FinalCTA() {
  return (
    <section className={styles.section}>
      <div className="container">
        <div className={styles.band}>
          <h2 className={styles.title}>
            <Translate id="homepage.finalcta.title">
              지금, 첫 단계부터 시작하세요
            </Translate>
          </h2>
          <p className={styles.subtitle}>
            <Translate id="homepage.finalcta.subtitle">
              OpenChain KWG 기반 무료 가이드로 자체 인증 선언까지 갑니다.
              가이드와 템플릿은 모두 무료이고 벤더 종속이 없습니다.
            </Translate>
          </p>
          <div className={styles.ctas}>
            <Link className={styles.primary} to="/docs">
              {translate({
                id: 'homepage.finalcta.cta',
                message: '가이드 시작하기',
              })}
            </Link>
            <Link className={styles.secondary} to="/reference/intro">
              {translate({
                id: 'homepage.finalcta.cta2',
                message: '산출물 샘플 보기',
              })}
            </Link>
          </div>
          <p className={styles.note}>
            <Translate id="homepage.finalcta.note">
              인증 이후 취약점·라이선스·SBOM을 상시 모니터링하고 싶다면
            </Translate>{' '}
            <Link
              href="https://trustedoss.github.io/trusca/"
              className={styles.noteLink}>
              TRUSCA
            </Link>
            <Translate id="homepage.finalcta.note.suffix">
              를 확인하세요.
            </Translate>
          </p>
        </div>
      </div>
    </section>
  );
}

export default FinalCTA;
