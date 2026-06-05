/**
 * trustedoss JourneyProgress — 0에서 자체 인증까지 7단계 진행 가시화
 * 진행 상태는 브라우저 localStorage에 저장된다(서버 렌더 시 빈 상태).
 * CC BY 4.0 · OpenChain KWG · haksungjang
 */

import React, {useEffect, useState} from 'react';
import Link from '@docusaurus/Link';
import Translate, {translate} from '@docusaurus/Translate';

import styles from './styles.module.css';

type Step = {
  id: string;
  label: string;
  href: string;
};

const STEPS: Step[] = [
  {
    id: 'organization',
    label: translate({
      id: 'journey.step.organization',
      message: '2. 조직 구성',
    }),
    href: '/docs/organization',
  },
  {
    id: 'policy',
    label: translate({id: 'journey.step.policy', message: '3. 오픈소스 정책'}),
    href: '/docs/policy',
  },
  {
    id: 'process',
    label: translate({id: 'journey.step.process', message: '4. 프로세스'}),
    href: '/docs/process',
  },
  {
    id: 'sbom',
    label: translate({id: 'journey.step.sbom', message: '5. SBOM 생성'}),
    href: '/docs/tools/sbom-generation',
  },
  {
    id: 'vulnerability',
    label: translate({
      id: 'journey.step.vulnerability',
      message: '5. 취약점 대응',
    }),
    href: '/docs/tools/vulnerability',
  },
  {
    id: 'training',
    label: translate({id: 'journey.step.training', message: '6. 교육 체계'}),
    href: '/docs/training',
  },
  {
    id: 'conformance',
    label: translate({id: 'journey.step.conformance', message: '7. 자체 인증'}),
    href: '/docs/conformance',
  },
];

const STORAGE_KEY = 'trustedoss-journey-progress';

function JourneyProgress() {
  const [done, setDone] = useState<string[]>([]);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed)) {
          setDone(parsed.filter(id => typeof id === 'string'));
        }
      }
    } catch {
      // localStorage 접근 불가 시 빈 상태 유지
    }
    setLoaded(true);
  }, []);

  function toggle(id: string) {
    setDone(prev => {
      const next = prev.includes(id)
        ? prev.filter(x => x !== id)
        : [...prev, id];
      try {
        window.localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      } catch {
        // 저장 실패는 무시
      }
      return next;
    });
  }

  const count = done.length;
  const pct = Math.round((count / STEPS.length) * 100);

  return (
    <div className={styles.journey}>
      <div className={styles.header}>
        <span className={styles.title}>
          <Translate id="journey.title">0에서 자체 인증까지</Translate>
        </span>
        <span className={styles.count} aria-live="polite">
          {count} / {STEPS.length}
        </span>
      </div>
      <div
        className={styles.bar}
        role="progressbar"
        aria-valuenow={pct}
        aria-valuemin={0}
        aria-valuemax={100}>
        <div className={styles.fill} style={{width: `${pct}%`}} />
      </div>
      <ol className={styles.steps}>
        {STEPS.map(step => {
          const isDone = done.includes(step.id);
          return (
            <li
              key={step.id}
              className={isDone ? styles.stepDone : styles.step}>
              <button
                type="button"
                className={styles.check}
                aria-pressed={isDone}
                aria-label={translate(
                  {id: 'journey.toggle', message: '{label} 완료 표시 전환'},
                  {label: step.label}
                )}
                onClick={() => toggle(step.id)}
                disabled={!loaded}>
                {isDone ? '✓' : ''}
              </button>
              <Link to={step.href} className={styles.stepLabel}>
                {step.label}
              </Link>
            </li>
          );
        })}
      </ol>
      <p className={styles.note}>
        <Translate id="journey.note">
          체크는 이 브라우저에만 저장됩니다. 단계를 마칠 때마다 표시해 진행
          상황을 추적하세요.
        </Translate>
      </p>
    </div>
  );
}

export default JourneyProgress;
