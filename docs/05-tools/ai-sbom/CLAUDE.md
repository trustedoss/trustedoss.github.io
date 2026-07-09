# 챕터 05-4 — AI SBOM (선택)

## 현재 위치: 5단계 도구 챕터의 선택 확장

AI 시스템(모델 개발·도입)을 다루는 조직만 진행하는 선택 챕터다.
HuggingFace 모델의 CycloneDX ML-BOM 생성을 실습한다.

## 이 챕터의 목표

- 일반 SBOM 과 AI SBOM 의 차이(모델·데이터셋 라이선스)를 이해한다
- BomLens 로 모델 ML-BOM 을 생성하고 라이선스 항목을 허용 목록과 대조한다

## 전제 조건

- 5.1 SBOM 생성 완료 (SBOM 개념·도구 숙지)
- Docker 실행 환경, 네트워크 연결

## 충족되는 체크리스트 항목

필수 항목을 직접 충족하지 않는다 (선택 확장). 모델·데이터셋을 제품에 포함해 공급하는 경우
G3B 계열(SBOM)의 범위를 AI 컴포넌트로 확장 적용하는 취지다.

## 도구

- 메인: BomLens (github.com/sktelecom/sbom-tools) — `--model` 옵션으로 HuggingFace 모델 스캔
- 대안: OWASP AIBOM Generator — KWG AI SBOM 가이드 참조

## 산출물

실습 산출물은 sbom-tools 클론 디렉토리에 생성된다 (`{project}_{version}_bom.json` 등).
output/ 필수 산출물 체계에는 포함되지 않는다 (선택 챕터).

## 자주 발생하는 문제

**Q: 모델 스캔에 시간이 오래 걸립니다.**
A: 첫 실행은 전용 이미지(bomlens-aibom) 다운로드가 있어 오래 걸린다. 이후 실행은 빨라진다.

**Q: ML-BOM 의 라이선스 항목이 비어 있습니다.**
A: 모델 카드에 라이선스가 선언되지 않은 경우다. HuggingFace 모델 페이지에서 직접 확인하고
보완 기록을 남기는 것 자체가 이 실습의 학습 포인트다.
