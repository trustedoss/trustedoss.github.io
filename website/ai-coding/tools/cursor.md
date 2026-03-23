---
id: cursor
title: Cursor
sidebar_label: Cursor
sidebar_position: 2
---

# Cursor

Cursor는 AI 기능이 내장된 코드 편집기입니다. VS Code를 기반으로 하며, AI 페어 프로그래밍 기능을 제공합니다.

## 설치

[cursor.com](https://www.cursor.com)에서 다운로드합니다.

## 오픈소스 컴플라이언스 설정

### .cursorrules 파일

프로젝트 루트에 `.cursorrules` 파일을 생성하여 오픈소스 컴플라이언스 규칙을 정의합니다:

```
# 오픈소스 컴플라이언스 Rules

## 의존성 관리
- 새 패키지 추가 전 라이선스 확인 필수 (허용: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause)
- GPL/LGPL/AGPL 라이선스는 법무팀 검토 후 추가
- 패키지 추가 후 SBOM 업데이트 알림 제공

## 코드 생성
- 저작권 표시가 있는 코드 복사 시 라이선스 확인
- 새 파일 생성 시 프로젝트 라이선스 헤더 포함

## 보안
- 알려진 취약점(CVE)이 있는 패키지 버전 사용 금지
- 의존성 업데이트 시 변경 내역 확인 권장
```

## 관련 링크

- [Cursor 공식 문서](https://docs.cursor.com)
- [공통 Rules 템플릿](../rules-template)
