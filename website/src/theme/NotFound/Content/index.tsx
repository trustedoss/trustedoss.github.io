/**
 * 404 페이지. 진단 B-10 은 기본 404 에 복귀 동선이 없고(검색창도 주요 링크도 없다),
 * 제목과 본문이 같은 말을 두 번 하며, 문서용 헤딩 복사 버튼이 붙는다고 지적했다.
 * 여기서 검색창, 네 인스턴스 링크, 문장 하나로 바꾼다. 제목은 `@theme/Heading` 이
 * 아니라 순수 `h1` 이라 복사 버튼이 붙지 않는다.
 */

import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import Translate, {translate} from '@docusaurus/Translate';
import SearchBar from '@theme/SearchBar';

import styles from './styles.module.css';

type Destination = {
  href: string;
  title: string;
  desc: string;
};

function useDestinations(): Destination[] {
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

export default function NotFoundContent({
  className,
}: {
  className?: string;
}): JSX.Element {
  const destinations = useDestinations();

  return (
    <main className={clsx(styles.wrap, className)}>
      <p className={styles.code}>404</p>
      <h1 className={styles.title}>
        {/* `theme.NotFound.title` 은 Docusaurus 가 로케일별 번역을 이미 갖고 있어
            인라인 기본값이 무시된다. 그래서 theme.* 밖의 id 를 쓴다. */}
        <Translate id="notFound.title" description="The title of the 404 page">
          찾으시는 페이지가 없습니다
        </Translate>
      </h1>
      <p className={styles.lead}>
        <Translate
          id="notFound.lead"
          description="The single explanatory sentence on the 404 page">
          주소가 바뀌었거나 삭제된 페이지입니다. 검색하거나 아래에서 골라
          이어가세요.
        </Translate>
      </p>

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
