/**
 * trustedoss Term — 용어 호버/포커스 툴팁
 * 사용: <Term k="sbom">SBOM</Term>  또는  <Term def="설명">용어</Term>
 * 초심자가 본문에서 약어 위에 마우스를 올리거나 포커스하면 풀이가 뜬다.
 * CC BY 4.0 · OpenChain KWG · haksungjang
 */

import React from 'react';
import {GLOSSARY} from '@site/src/data/glossary';

import styles from './styles.module.css';

function Term({
  k,
  def,
  children,
}: {
  k?: string;
  def?: string;
  children: React.ReactNode;
}) {
  const text = def ?? (k ? GLOSSARY[k] : undefined);
  if (!text) {
    return <>{children}</>;
  }
  return (
    <span className={styles.term} tabIndex={0}>
      {children}
      <span className={styles.tip} role="tooltip">
        {text}
      </span>
    </span>
  );
}

export default Term;
