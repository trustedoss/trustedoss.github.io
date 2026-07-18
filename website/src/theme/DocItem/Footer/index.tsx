import React from 'react';
import clsx from 'clsx';
import {ThemeClassNames} from '@docusaurus/theme-common';
import {useDoc} from '@docusaurus/plugin-content-docs/client';
import Translate from '@docusaurus/Translate';
import IconEdit from '@theme/Icon/Edit';
import LastUpdated from '@theme/LastUpdated';
import Link from '@docusaurus/Link';
import TagsListInline, {
  Props as TagsListInlineProps,
} from '@theme/TagsListInline';

import styles from './styles.module.css';
import DocsRating from '../../../../core/DocsRating';

function TagsRow(props: TagsListInlineProps) {
  return (
    <div
      className={clsx(
        ThemeClassNames.docs.docFooterTagsRow,
        'row margin-bottom--sm'
      )}>
      <div className="col">
        <TagsListInline {...props} />
      </div>
    </div>
  );
}
function EditPage({label, href}: {label: string; href: string}) {
  return (
    <Link to={href} className={ThemeClassNames.common.editThisPage}>
      <IconEdit />
      <Translate
        id="theme.common.editThisPage"
        description="The link label to edit the page">
        {label}
      </Translate>
    </Link>
  );
}
type EditUrlButton = {label: string; href: string};

function EditMetaRow({editUrl, lastUpdatedAt, lastUpdatedBy}) {
  const buttons = React.useMemo((): EditUrlButton[] => {
    // editUrl은 일반 URL 문자열이 기본이고, JSON 배열([{label, href}]) 형식도 허용한다
    if (editUrl?.trim().startsWith('[')) {
      try {
        return JSON.parse(editUrl);
      } catch {
        // JSON 형식이 아니면 아래의 일반 URL 처리로 폴백
      }
    }
    return [{href: editUrl, label: 'Edit this page'}];
  }, [editUrl]);
  return (
    <div className={clsx(ThemeClassNames.docs.docFooterEditMetaRow, 'row')}>
      <div className={clsx(styles.editButtons)}>
        {buttons.map(({label, href}, index) => (
          <EditPage key={index} label={label} href={href} />
        ))}
      </div>
      <div className={clsx(styles.lastUpdated)}>
        {(lastUpdatedAt || lastUpdatedBy) && (
          <LastUpdated
            lastUpdatedAt={lastUpdatedAt}
            lastUpdatedBy={lastUpdatedBy}
          />
        )}
      </div>
    </div>
  );
}
export default function DocItemFooter() {
  const {metadata} = useDoc();
  const {editUrl, lastUpdatedAt, lastUpdatedBy, tags} = metadata;
  const canDisplayTagsRow = tags.length > 0;
  const canDisplayEditMetaRow = !!(editUrl || lastUpdatedAt || lastUpdatedBy);
  const canDisplayFooter = canDisplayTagsRow || canDisplayEditMetaRow;
  if (!canDisplayFooter) {
    return null;
  }

  return (
    <>
      <DocsRating label={metadata.id} />
      <footer
        className={clsx(ThemeClassNames.docs.docFooter, 'docusaurus-mt-lg')}>
        {canDisplayTagsRow && <TagsRow tags={tags} />}
        {canDisplayEditMetaRow && (
          <EditMetaRow
            editUrl={editUrl}
            lastUpdatedAt={lastUpdatedAt}
            lastUpdatedBy={lastUpdatedBy}
          />
        )}
      </footer>
    </>
  );
}
