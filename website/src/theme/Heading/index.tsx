/**
 * Heading 스위즐
 * Gemini docs처럼 제목·헤딩 옆에 "링크 복사" 버튼을 단다.
 * - 페이지 제목(h1): 항상 보이는 복사 버튼(페이지 URL 복사)
 * - h2~h6: hover 시 복사 버튼(해당 섹션 앵커 URL 복사)
 * 기본 동작(앵커 등록, sticky navbar 오프셋 클래스)은 유지한다.
 */
import React, {useCallback, useState} from 'react';
import clsx from 'clsx';
import {useAnchorTargetClassName} from '@docusaurus/theme-common';
import useBrokenLinks from '@docusaurus/useBrokenLinks';
import type {Props} from '@theme/Heading';

import styles from './styles.module.css';

function CopyLinkButton({anchor}: {anchor?: string}): JSX.Element {
  const [copied, setCopied] = useState(false);
  const onClick = useCallback(() => {
    if (typeof window === 'undefined') {
      return;
    }
    const {origin, pathname, href} = window.location;
    const url = anchor ? `${origin}${pathname}#${anchor}` : href.split('#')[0];
    window.navigator?.clipboard?.writeText(url);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1500);
  }, [anchor]);
  return (
    <button
      type="button"
      className={clsx(styles.copyBtn, copied && styles.copied)}
      onClick={onClick}
      aria-label="링크 복사"
      title={copied ? '복사됨' : '링크 복사'}>
      <span className={styles.icon} aria-hidden="true" />
    </button>
  );
}

export default function Heading({as: As, id, ...props}: Props): JSX.Element {
  const brokenLinks = useBrokenLinks();
  const anchorTargetClassName = useAnchorTargetClassName(id);

  // 페이지 제목(h1): 앵커 없음. 항상 보이는 페이지 링크 복사 버튼.
  if (As === 'h1') {
    return (
      <As
        {...props}
        id={undefined}
        className={clsx(styles.title, props.className)}>
        {props.children}
        <CopyLinkButton />
      </As>
    );
  }

  // id 없는 헤딩은 기본 렌더
  if (!id) {
    return <As {...props} id={undefined} />;
  }

  brokenLinks.collectAnchor(id);

  return (
    <As
      {...props}
      className={clsx(
        'anchor',
        styles.heading,
        anchorTargetClassName,
        props.className
      )}
      id={id}>
      {props.children}
      <CopyLinkButton anchor={id} />
    </As>
  );
}
