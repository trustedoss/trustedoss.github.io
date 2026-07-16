/**
 * legacy-parser — 라이선스 미명시 패키지 재현용 실습 모듈.
 * package.json에 license 필드가 없어, SBOM에서 라이선스 미식별로 표시됩니다.
 */

function parseGreeting(text) {
  return String(text).trim().toUpperCase();
}

module.exports = {parseGreeting};
