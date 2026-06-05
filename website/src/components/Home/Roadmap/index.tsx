/**
 * trustedoss.dev Roadmap Component — 셀프스터디 학습 여정(우리 고유 콘텐츠)
 * CC BY 4.0 · OpenChain KWG · haksungjang
 */

import React from 'react';
import Link from '@docusaurus/Link';
import Translate, {translate} from '@docusaurus/Translate';

import styles from './styles.module.css';

type Step = {
  no: string;
  title: string;
  desc: string;
  href: string;
};

const STEPS: Step[] = [
  {
    no: '00',
    title: translate({id: 'homepage.roadmap.s0.title', message: '시작하기'}),
    desc: translate({
      id: 'homepage.roadmap.s0.desc',
      message: '공급망 보안과 두 표준의 큰 그림을 잡습니다.',
    }),
    href: '/docs',
  },
  {
    no: '01',
    title: translate({id: 'homepage.roadmap.s1.title', message: '환경 준비'}),
    desc: translate({
      id: 'homepage.roadmap.s1.desc',
      message: '셀프스터디와 산출물 생성을 위한 기반을 갖춥니다.',
    }),
    href: '/docs/setup',
  },
  {
    no: '02',
    title: translate({id: 'homepage.roadmap.s2.title', message: '조직 구성'}),
    desc: translate({
      id: 'homepage.roadmap.s2.desc',
      message: '책임 체계와 RACI로 거버넌스 주체를 정합니다.',
    }),
    href: '/docs/organization',
  },
  {
    no: '03',
    title: translate({
      id: 'homepage.roadmap.s3.title',
      message: '오픈소스 정책',
    }),
    desc: translate({
      id: 'homepage.roadmap.s3.desc',
      message: '라이선스 승인 등급과 정책 문서를 수립합니다.',
    }),
    href: '/docs/policy',
  },
  {
    no: '04',
    title: translate({id: 'homepage.roadmap.s4.title', message: '프로세스'}),
    desc: translate({
      id: 'homepage.roadmap.s4.desc',
      message: '검토·승인·공개로 이어지는 운영 절차를 설계합니다.',
    }),
    href: '/docs/process',
  },
  {
    no: '05',
    title: translate({
      id: 'homepage.roadmap.s5.title',
      message: 'SBOM · 취약점',
    }),
    desc: translate({
      id: 'homepage.roadmap.s5.desc',
      message: 'SBOM 생성·분석과 취약점 관리를 도구로 실행합니다.',
    }),
    href: '/docs/tools/sbom-generation',
  },
  {
    no: '06',
    title: translate({id: 'homepage.roadmap.s6.title', message: '교육 체계'}),
    desc: translate({
      id: 'homepage.roadmap.s6.desc',
      message: '구성원이 체계를 지속 운영하도록 역량을 갖춥니다.',
    }),
    href: '/docs/training',
  },
  {
    no: '07',
    title: translate({id: 'homepage.roadmap.s7.title', message: '자체 인증'}),
    desc: translate({
      id: 'homepage.roadmap.s7.desc',
      message: '적합성을 점검하고 자체 인증 선언까지 마칩니다.',
    }),
    href: '/docs/conformance',
  },
];

function Roadmap() {
  return (
    <section className={styles.roadmap}>
      <div className="container">
        <header className={styles.sectionHeader}>
          <h2>
            <Translate id="homepage.roadmap.title">
              0에서 자체 인증까지, 단계별 여정
            </Translate>
          </h2>
          <p>
            <Translate id="homepage.roadmap.subtitle">
              순서대로 따라가면 됩니다. 각 단계의 에이전트가 회사 맞춤 산출물을
              만들어 줍니다.
            </Translate>
          </p>
        </header>
        <ol className={styles.grid}>
          {STEPS.map(step => (
            <li key={step.no} className={styles.step}>
              <Link to={step.href} className={styles.stepCard}>
                <div className={styles.stepTop}>
                  <span className={styles.stepNo}>{step.no}</span>
                  <span className={styles.arrow} aria-hidden="true">
                    →
                  </span>
                </div>
                <h3 className={styles.stepTitle}>{step.title}</h3>
                <p className={styles.stepDesc}>{step.desc}</p>
              </Link>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}

export default Roadmap;
