/**
 * trustedoss.dev Showcase — 에이전트 산출물 미리보기 (Vercel풍 코드 카드)
 * CC BY 4.0 · OpenChain KWG · haksungjang
 */

import React from 'react';
import Link from '@docusaurus/Link';
import Translate, {translate} from '@docusaurus/Translate';

import styles from './styles.module.css';

type Shot = {
  id: string;
  href: string;
  file: string;
  preview: string;
  caption: string;
};

const SHOTS: Shot[] = [
  {
    id: 'policy',
    href: '/reference/samples/policy',
    file: 'oss-policy.md',
    preview: `# 오픈소스 정책
## 3.1 라이선스 승인 등급
- 허용:   MIT · Apache-2.0
- 조건부: LGPL · MPL-2.0
- 금지:   AGPL · 상용 EULA`,
    caption: translate({
      id: 'homepage.showcase.policy.caption',
      message: '정책 · 조직 — 라이선스 승인 등급과 RACI 책임 매트릭스',
    }),
  },
  {
    id: 'sbom',
    href: '/reference/samples/sbom',
    file: 'sbom.cdx.json',
    preview: `{
  "bomFormat": "CycloneDX",
  "components": [
    { "name": "log4j-core",
      "version": "2.14.1",
      "vuln": "CVE-2021-44228" }
  ]
}`,
    caption: translate({
      id: 'homepage.showcase.sbom.caption',
      message: 'SBOM · 취약점 — CycloneDX 분석과 취약점 트리에이지 리포트',
    }),
  },
  {
    id: 'conformance',
    href: '/reference/samples/conformance',
    file: 'conformance.md',
    preview: `ISO/IEC 5230 적합성 선언문
조직: ____________________
[v] 3.1 프로그램 기반 수립
[v] 3.2 업무 지원 · 책임 지정
[v] 3.3 콘텐츠 검토 · 승인`,
    caption: translate({
      id: 'homepage.showcase.conformance.caption',
      message: '자체 인증 — 적합성 체크리스트와 자체 인증 선언문 초안',
    }),
  },
];

function ShotFigure({shot}: {shot: Shot}) {
  return (
    <figure className={styles.shot}>
      <Link to={shot.href} className={styles.frame}>
        <div className={styles.bar}>
          <span className={styles.dots} aria-hidden="true">
            <i />
            <i />
            <i />
          </span>
          <span className={styles.file}>{shot.file}</span>
        </div>
        <pre className={styles.preview}>
          <code>{shot.preview}</code>
        </pre>
      </Link>
      <figcaption className={styles.caption}>{shot.caption}</figcaption>
    </figure>
  );
}

function Showcase() {
  return (
    <section className={styles.showcase}>
      <div className="container">
        <header className={styles.sectionHeader}>
          <h2>
            <Translate id="homepage.showcase.title">
              에이전트가 만드는 실제 산출물
            </Translate>
          </h2>
          <p>
            <Translate id="homepage.showcase.subtitle">
              회사 맞춤으로 자동 생성되는 산출물을 Best Practice 샘플로 미리
              보세요.
            </Translate>
          </p>
        </header>
        <div className={styles.grid}>
          {SHOTS.map(shot => (
            <ShotFigure key={shot.id} shot={shot} />
          ))}
        </div>
      </div>
    </section>
  );
}

export default Showcase;
