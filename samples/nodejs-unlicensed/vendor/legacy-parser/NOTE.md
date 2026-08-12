# 이 패키지에 license 필드가 없는 이유

이 패키지는 **라이선스 미명시 패키지를 재현하기 위한 실습용 가짜 패키지**입니다.
package.json에 license 필드가 의도적으로 없으며, SBOM 생성 시 라이선스 정보가
비어 있거나(CycloneDX) `NOASSERTION`(SPDX)으로 표시됩니다.

실제 npm 레지스트리 패키지를 쓰지 않는 이유: 레지스트리 패키지는 배포자가 나중에
라이선스를 추가하면 실습 결과가 재현되지 않기 때문입니다.

---

## Why this package has no license field

This is a **fake package that stands in for one with no declared license**.
The license field is left out of package.json on purpose, so the SBOM reports the
license as empty (CycloneDX) or `NOASSERTION` (SPDX).

A real npm registry package is not used here because its publisher could add a
license later, and the exercise would stop reproducing the same result.
