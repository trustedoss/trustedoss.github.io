/**
 * SampleDemo — 무API키 샘플 체험
 *
 * SBOM 분석기가 무엇을 해주는지 API 키 없이 즉시 체감하도록,
 * 미리 만든(canned) 샘플 SBOM과 그 분석 결과를 보여준다.
 * 실제 분석은 페이지 하단의 브라우저 도구(본인 API 키 입력)로 진행한다.
 *
 * 데이터는 output-sample/sbom/fixture-sample.cdx.json 의 컴포넌트 구성을 따른다.
 * CVE는 해당 버전의 실제 공개 취약점이다.
 */

import React, {useState} from 'react';
import styles from './styles.module.css';

type Component = {
  name: string;
  version: string;
  license: string;
  cls: '허용형(Permissive)' | '강한 카피레프트(Strong Copyleft)';
};

type Finding = {
  pkg: string;
  cve: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low';
  cvss: string;
  fix: string;
};

const SAMPLE_COMPONENTS: Component[] = [
  {name: 'PyYAML', version: '5.3.1', license: 'MIT', cls: '허용형(Permissive)'},
  {
    name: 'requests',
    version: '2.27.0',
    license: 'Apache-2.0',
    cls: '허용형(Permissive)',
  },
  {
    name: 'celery',
    version: '5.2.0',
    license: 'BSD-3-Clause',
    cls: '허용형(Permissive)',
  },
  {
    name: 'mysql-connector-python',
    version: '8.1.0',
    license: 'GPL-2.0-only',
    cls: '강한 카피레프트(Strong Copyleft)',
  },
  {
    name: 'Pillow',
    version: '9.0.0',
    license: 'HPND',
    cls: '허용형(Permissive)',
  },
];

const SAMPLE_FINDINGS: Finding[] = [
  {
    pkg: 'PyYAML 5.3.1',
    cve: 'CVE-2020-14343',
    severity: 'Critical',
    cvss: '9.8',
    fix: '5.4 이상',
  },
  {
    pkg: 'requests 2.27.0',
    cve: 'CVE-2023-32681',
    severity: 'Medium',
    cvss: '6.1',
    fix: '2.31.0 이상',
  },
];

const SEVERITY_CLASS: Record<Finding['severity'], string> = {
  Critical: styles.sevCritical,
  High: styles.sevHigh,
  Medium: styles.sevMedium,
  Low: styles.sevLow,
};

export default function SampleDemo(): JSX.Element {
  const [shown, setShown] = useState(false);

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <span className={styles.badge}>API 키 불필요</span>
        <strong>샘플로 미리보기</strong>
      </div>

      <p className={styles.intro}>
        미리 준비한 샘플 SBOM을 분석한 결과를 API 호출 없이 바로 보여줍니다.
        도구가 어떤 결과를 만들어 주는지 먼저 확인하세요. 내 SBOM으로 실제
        분석하려면 아래 도구에 본인 API 키를 입력하면 됩니다.
      </p>

      <div className={styles.panel}>
        <div className={styles.panelTitle}>입력 — 샘플 SBOM (5개 컴포넌트)</div>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>컴포넌트</th>
              <th>버전</th>
              <th>라이선스</th>
              <th>분류</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_COMPONENTS.map(c => (
              <tr key={c.name}>
                <td>
                  <code>{c.name}</code>
                </td>
                <td>{c.version}</td>
                <td>{c.license}</td>
                <td>{c.cls}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {!shown ? (
        <button
          type="button"
          className={styles.runButton}
          onClick={() => setShown(true)}>
          샘플 분석 결과 보기
        </button>
      ) : (
        <div className={styles.panel}>
          <div className={styles.panelTitle}>결과 — 분석 리포트 (예시)</div>

          <p className={styles.resultLine}>
            <strong>라이선스 요약</strong> — 허용형
            4건(MIT·Apache-2.0·BSD-3-Clause·HPND), 강한 카피레프트 1건.
          </p>

          <div className={styles.copyleft}>
            <strong>카피레프트 위험 1건</strong>
            <br />
            <code>mysql-connector-python 8.1.0</code> 는 GPL-2.0-only
            라이선스입니다. 배포 방식에 따라 전체 소스 공개 의무가 생길 수 있어
            검토가 필요합니다. 대안: PyMySQL(MIT), aiomysql(MIT).
          </div>

          <div className={styles.panelTitle}>알려진 취약점</div>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>패키지</th>
                <th>CVE</th>
                <th>심각도</th>
                <th>CVSS</th>
                <th>수정 버전</th>
              </tr>
            </thead>
            <tbody>
              {SAMPLE_FINDINGS.map(f => (
                <tr key={f.cve}>
                  <td>
                    <code>{f.pkg}</code>
                  </td>
                  <td>{f.cve}</td>
                  <td>
                    <span
                      className={`${styles.sev} ${SEVERITY_CLASS[f.severity]}`}>
                      {f.severity}
                    </span>
                  </td>
                  <td>{f.cvss}</td>
                  <td>{f.fix}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <p className={styles.resultLine}>
            <strong>권고</strong> — Critical(CVE-2020-14343)부터 즉시 패치하고,
            카피레프트 컴포넌트는 배포 전 법무 검토 또는 대안 교체를 진행합니다.
          </p>

          <p className={styles.note}>
            위 결과는 샘플 SBOM 기준 예시입니다. 실제 프로젝트 결과는 아래
            도구에서 본인 SBOM을 업로드해 확인하세요.
          </p>
        </div>
      )}
    </div>
  );
}
