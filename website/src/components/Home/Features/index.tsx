/**
 * trustedoss.dev Features — 세 트랙 (Vercel풍 카드)
 * CC BY 4.0 · OpenChain KWG · haksungjang
 */

import React from 'react';
import Link from '@docusaurus/Link';
import Translate, {translate} from '@docusaurus/Translate';

import styles from './styles.module.css';

type IconName = 'governance' | 'devsecops' | 'aicoding';

function FeatureIcon({name}: {name: IconName}) {
  const p = {
    width: 22,
    height: 22,
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    strokeWidth: 1.7,
    strokeLinecap: 'round' as const,
    strokeLinejoin: 'round' as const,
    'aria-hidden': true,
  };
  if (name === 'governance') {
    return (
      <svg {...p}>
        <path d="M3 21h18" />
        <path d="M5 21V8l7-4 7 4v13" />
        <path d="M9 21v-6h6v6" />
      </svg>
    );
  }
  if (name === 'devsecops') {
    return (
      <svg {...p}>
        <path d="M12 3l7 3v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z" />
        <path d="M9.5 12l1.8 1.8L15 10" />
      </svg>
    );
  }
  return (
    <svg {...p}>
      <rect x="4" y="7" width="16" height="12" rx="2" />
      <path d="M12 7V4M9.2 12h.01M14.8 12h.01M9.5 16h5" />
      <path d="M2 12h2M20 12h2" />
    </svg>
  );
}

type Track = {
  id: string;
  icon: IconName;
  title: string;
  desc: string;
  href: string;
};

const TRACKS: Track[] = [
  {
    id: 'governance',
    icon: 'governance',
    title: translate({id: 'homepage.cta.feature1.title', message: '체계구축'}),
    desc: translate({
      id: 'homepage.cta.feature1.desc',
      message:
        'ISO/IEC 5230 & 18974 기반으로 기업 오픈소스 관리 체계를 처음부터 완성까지 구축합니다.',
    }),
    href: '/docs',
  },
  {
    id: 'devsecops',
    icon: 'devsecops',
    title: translate({id: 'homepage.cta.feature2.title', message: 'DevSecOps'}),
    desc: translate({
      id: 'homepage.cta.feature2.desc',
      message:
        '개발 파이프라인에 보안을 통합합니다. SAST, SCA, 컨테이너 보안, CI/CD 자동화를 다룹니다.',
    }),
    href: '/devsecops/intro',
  },
  {
    id: 'aicoding',
    icon: 'aicoding',
    title: translate({id: 'homepage.cta.feature3.title', message: 'AI코딩'}),
    desc: translate({
      id: 'homepage.cta.feature3.desc',
      message:
        'Claude Code, Cursor, Copilot 등 AI 코딩 도구와 오픈소스 컴플라이언스를 함께 관리합니다.',
    }),
    href: '/ai-coding/intro',
  },
];

function TrackCard({icon, title, desc, href}: Track) {
  return (
    <Link to={href} className={styles.card}>
      <span className={styles.icon}>
        <FeatureIcon name={icon} />
      </span>
      <h3 className={styles.title}>{title}</h3>
      <p className={styles.desc}>{desc}</p>
      <span className={styles.more}>
        <Translate id="homepage.feature.more">자세히 보기</Translate>
        <span aria-hidden="true"> →</span>
      </span>
    </Link>
  );
}

function Features() {
  return (
    <section className={styles.features}>
      <div className="container">
        <header className={styles.sectionHeader}>
          <h2>
            <Translate id="homepage.features.title">
              하나의 가이드, 세 갈래의 길
            </Translate>
          </h2>
          <p>
            <Translate id="homepage.features.subtitle">
              표준 기반 관리 체계, 보안 파이프라인, AI 코딩 컴플라이언스 —
              역할에 맞는 길을 따라가세요.
            </Translate>
          </p>
        </header>
        <div className={styles.grid}>
          {TRACKS.map(track => (
            <TrackCard key={track.id} {...track} />
          ))}
        </div>
      </div>
    </section>
  );
}

export default Features;
