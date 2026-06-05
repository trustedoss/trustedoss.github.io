/**
 * trustedoss Prerequisite — 챕터 상단 전제 조건 배지
 * 사용 예: <Prerequisite items={[{label: '2. 조직 구성', href: '/docs/organization'}]} />
 *          <Prerequisite>없음 — 여기가 시작점입니다.</Prerequisite>
 * CC BY 4.0 · OpenChain KWG · haksungjang
 */

import React from 'react';
import Link from '@docusaurus/Link';
import Translate from '@docusaurus/Translate';

import styles from './styles.module.css';

type Item = {label: string; href?: string};

function Prerequisite({
  items,
  children,
}: {
  items?: Item[];
  children?: React.ReactNode;
}) {
  return (
    <aside className={styles.prereq} aria-label="전제 조건">
      <span className={styles.badge}>
        <Translate id="prerequisite.label">전제 조건</Translate>
      </span>
      <span className={styles.body}>
        {items?.map((it, i) => (
          <React.Fragment key={i}>
            {i > 0 && <span className={styles.sep}>, </span>}
            {it.href ? <Link to={it.href}>{it.label}</Link> : it.label}
          </React.Fragment>
        ))}
        {items && items.length > 0 && children ? (
          <span className={styles.sep}> · </span>
        ) : null}
        {children}
      </span>
    </aside>
  );
}

export default Prerequisite;
