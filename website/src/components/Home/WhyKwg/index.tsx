/**
 * trustedoss.dev WhyKwg — OpenChain KWG와의 보완 관계/차별화
 * CC BY 4.0 · OpenChain KWG · haksungjang
 */

import React from 'react';
import Link from '@docusaurus/Link';
import Translate, {translate} from '@docusaurus/Translate';

import styles from './styles.module.css';

type Side = {
  id: string;
  badge: string;
  title: string;
  desc: string;
  points: string[];
};

const SIDES: Side[] = [
  {
    id: 'kwg',
    badge: translate({id: 'homepage.whykwg.kwg.badge', message: '무엇을, 왜'}),
    title: translate({
      id: 'homepage.whykwg.kwg.title',
      message: 'OpenChain KWG',
    }),
    desc: translate({
      id: 'homepage.whykwg.kwg.desc',
      message:
        '표준이 요구하는 것과 그 이유를 알려줍니다. 국제 표준과 기업 OSS 관리 가이드, 빈 템플릿을 제공합니다.',
    }),
    points: [
      translate({
        id: 'homepage.whykwg.kwg.point1',
        message: 'ISO/IEC 5230과 18974 표준 가이드',
      }),
      translate({
        id: 'homepage.whykwg.kwg.point2',
        message: '정책과 프로세스 빈 템플릿',
      }),
      translate({
        id: 'homepage.whykwg.kwg.point3',
        message: '도구 가이드와 링크',
      }),
    ],
  },
  {
    id: 'trustedoss',
    badge: translate({
      id: 'homepage.whykwg.toss.badge',
      message: '어떻게, 자동으로',
    }),
    title: translate({id: 'homepage.whykwg.toss.title', message: 'TrustedOSS'}),
    desc: translate({
      id: 'homepage.whykwg.toss.desc',
      message:
        '그 표준을 AI와 자동화로 실제로 달성하게 합니다. 0에서 자체 인증까지 단일 동선으로 끌고 갑니다.',
    }),
    points: [
      translate({
        id: 'homepage.whykwg.toss.point1',
        message: 'AI 에이전트가 회사 맞춤 산출물을 자동 생성',
      }),
      translate({
        id: 'homepage.whykwg.toss.point2',
        message: '복붙 CI 워크플로와 Rules, 무API키 데모',
      }),
      translate({
        id: 'homepage.whykwg.toss.point3',
        message: 'DevSecOps와 AI 코딩 거버넌스까지 확장',
      }),
    ],
  },
];

function SideCard({badge, title, desc, points}: Side) {
  return (
    <div className={styles.card}>
      <span className={styles.badge}>{badge}</span>
      <h3 className={styles.title}>{title}</h3>
      <p className={styles.desc}>{desc}</p>
      <ul className={styles.points}>
        {points.map((p, i) => (
          <li key={i}>{p}</li>
        ))}
      </ul>
    </div>
  );
}

function WhyKwg() {
  return (
    <section className={styles.whyKwg}>
      <div className="container">
        <header className={styles.sectionHeader}>
          <h2>
            <Translate id="homepage.whykwg.title">
              왜 KWG와 함께 TrustedOSS인가
            </Translate>
          </h2>
          <p>
            <Translate id="homepage.whykwg.subtitle">
              경쟁이 아니라 보완입니다. KWG가 표준과 빈 템플릿으로 방향을
              제시하면, TrustedOSS는 그것을 AI와 자동화로 실행 가능한 산출물로
              만들어 줍니다.
            </Translate>
          </p>
        </header>
        <div className={styles.grid}>
          {SIDES.map(side => (
            <SideCard key={side.id} {...side} />
          ))}
        </div>
        <p className={styles.note}>
          <Translate id="homepage.whykwg.note">
            TrustedOSS는 KWG 콘텐츠를 동기화하며 CC BY 4.0 출처를 표기합니다.
          </Translate>{' '}
          <Link
            to="https://openchain-project.github.io/OpenChain-KWG/"
            className={styles.noteLink}>
            <Translate id="homepage.whykwg.note.link">
              OpenChain KWG 가이드 보기
            </Translate>
            <span aria-hidden="true"> →</span>
          </Link>
        </p>
      </div>
    </section>
  );
}

export default WhyKwg;
