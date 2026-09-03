/**
 * 404 페이지. 진단 B-10 은 기본 404 에 복귀 동선이 없고(검색창도 주요 링크도 없다),
 * 제목과 본문이 같은 말을 두 번 하며, 문서용 헤딩 복사 버튼이 붙는다고 지적했다.
 * 여기서 검색창, 네 인스턴스 링크, 문장 하나로 바꾼다. 제목은 `@theme/Heading` 이
 * 아니라 순수 `h1` 이라 복사 버튼이 붙지 않는다.
 *
 * 로케일 폴백(K15-a). GitHub Pages 는 없는 파일에 대해 요청 경로와 무관하게 루트
 * `404.html` 하나만 폴백으로 쓴다. `build/en/404.html` 이 따로 정상 생성돼 있어도
 * `/en/` 하위의 깨진 링크는 한국어 404 를 받는다. 서버가 경로 접두사를 보고 다른 파일을
 * 고르게 할 방법이 정적 호스팅엔 없으므로 클라이언트에서 판별한다.
 *
 * 리다이렉트가 아니라 같은 자리에서 영문으로 바꿔 그린다. 주소가 그대로 남아야 독자가
 * 어떤 링크가 끊겼는지 보고 고칠 수 있고, 리다이렉트 깜빡임도 없다. 찾지 못한 경로를
 * 화면에 함께 보여 준다.
 *
 * 하이드레이션. 서버가 그린 HTML 은 빌드 로케일(루트 폴백이면 한국어)이므로 첫 클라이언트
 * 렌더도 그대로 두고, 마운트 뒤에 상태를 바꿔 영문으로 교체한다.
 */

import React, {useEffect, useState} from 'react';
import clsx from 'clsx';
import Head from '@docusaurus/Head';
import Link from '@docusaurus/Link';
import Translate, {translate} from '@docusaurus/Translate';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import SearchBar from '@theme/SearchBar';

import styles from './styles.module.css';

type Destination = {
  href: string;
  title: string;
  desc: string;
};

/**
 * 영문 폴백 문구. 한국어 번들 안에서 쓰이므로 `translate()` 로는 얻을 수 없다.
 * `translate()` 는 빌드 시점에 로케일이 정해지는데, 여기서 필요한 것은 실행 시점 판별이다.
 * 문구를 바꾸면 `i18n/en/code.json` 의 `notFound.*` 도 같이 맞춰야 한다.
 */
const EN = {
  title: 'Page not found',
  lead: 'The address changed or the page was removed. Search, or pick one below to carry on.',
  requested: 'Could not find',
  destinations: [
    {
      href: '/en/docs',
      title: 'Open Source Management',
      desc: 'Build a system on ISO/IEC 5230 and 18974',
    },
    {
      href: '/en/devsecops/intro',
      title: 'DevSecOps',
      desc: 'Pipeline security and CI/CD automation',
    },
    {
      href: '/en/ai-coding/intro',
      title: 'AI Coding Governance',
      desc: 'Controls and regulation for AI coding tools',
    },
    {
      href: '/en/reference/intro',
      title: 'Reference',
      desc: 'Requirements matrix and deliverable samples',
    },
  ] as Destination[],
};

function useKoDestinations(): Destination[] {
  return [
    {
      href: '/docs',
      title: translate({
        id: 'notFound.link.docs.title',
        message: '오픈소스 관리',
      }),
      desc: translate({
        id: 'notFound.link.docs.desc',
        message: 'ISO/IEC 5230과 18974 기반 체계 구축',
      }),
    },
    {
      href: '/devsecops/intro',
      title: translate({
        id: 'notFound.link.devsecops.title',
        message: 'DevSecOps',
      }),
      desc: translate({
        id: 'notFound.link.devsecops.desc',
        message: '파이프라인 보안과 CI/CD 자동화',
      }),
    },
    {
      href: '/ai-coding/intro',
      title: translate({
        id: 'notFound.link.aicoding.title',
        message: 'AI 코딩 거버넌스',
      }),
      desc: translate({
        id: 'notFound.link.aicoding.desc',
        message: 'AI 코딩 도구의 통제와 규제 대응',
      }),
    },
    {
      href: '/reference/intro',
      title: translate({
        id: 'notFound.link.reference.title',
        message: '레퍼런스',
      }),
      desc: translate({
        id: 'notFound.link.reference.desc',
        message: '요구사항 매트릭스와 산출물 샘플',
      }),
    },
  ];
}

/** `/en/` 하위 경로를 한국어 번들이 폴백으로 받았는지. 마운트 뒤에만 참이 된다. */
function useEnglishFallback(): {active: boolean; path: string} {
  const {
    i18n: {currentLocale, defaultLocale},
  } = useDocusaurusContext();
  const [state, setState] = useState({active: false, path: ''});

  useEffect(() => {
    // 영문 번들이 직접 뜬 경우(`/en/404`)는 이미 영문이라 손댈 것이 없다.
    if (currentLocale !== defaultLocale) {
      return;
    }
    const {pathname} = window.location;
    if (pathname === '/en' || pathname.startsWith('/en/')) {
      setState({active: true, path: pathname});
    }
  }, [currentLocale, defaultLocale]);

  return state;
}

export default function NotFoundContent({
  className,
}: {
  className?: string;
}): JSX.Element {
  const koDestinations = useKoDestinations();
  const en = useEnglishFallback();
  const destinations = en.active ? EN.destinations : koDestinations;

  return (
    <main className={clsx(styles.wrap, className)}>
      {/* `lang` 과 `title` 은 Helmet 이 관리한다. DOM 을 직접 쓰면 다시 덮인다.
          실측으로 확인했다: 본문은 영문으로 바뀌는데 `lang` 은 ko, 제목은 한국어로 남았다. */}
      {en.active && (
        <Head>
          <html lang="en" />
          <title>{`${EN.title} · Trusted OSS`}</title>
        </Head>
      )}
      <p className={styles.code}>404</p>
      <h1 className={styles.title}>
        {en.active ? (
          EN.title
        ) : (
          /* `theme.NotFound.title` 은 Docusaurus 가 로케일별 번역을 이미 갖고 있어
             인라인 기본값이 무시된다. 그래서 theme.* 밖의 id 를 쓴다. */
          <Translate
            id="notFound.title"
            description="The title of the 404 page">
            찾으시는 페이지가 없습니다
          </Translate>
        )}
      </h1>
      <p className={styles.lead}>
        {en.active ? (
          EN.lead
        ) : (
          <Translate
            id="notFound.lead"
            description="The single explanatory sentence on the 404 page">
            주소가 바뀌었거나 삭제된 페이지입니다. 검색하거나 아래에서 골라
            이어가세요.
          </Translate>
        )}
      </p>

      {en.active && (
        <p className={styles.requested}>
          {EN.requested} <code>{en.path}</code>
        </p>
      )}

      <div className={styles.search}>
        <SearchBar />
      </div>

      <ul className={styles.grid}>
        {destinations.map(d => (
          <li key={d.href}>
            <Link to={d.href} className={styles.card}>
              <span className={styles.cardTitle}>{d.title}</span>
              <span className={styles.cardDesc}>{d.desc}</span>
            </Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
