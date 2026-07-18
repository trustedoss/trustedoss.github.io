/**
 * 마크다운 체크리스트(- [ ])가 라벨 없는 disabled checkbox로 렌더돼
 * 스크린리더가 "이름 없는 체크박스"로 읽는 문제 보정 — 항목 텍스트를
 * aria-label로 연결한다.
 */
export function onRouteDidUpdate(): void {
  document
    .querySelectorAll<HTMLInputElement>(
      'li.task-list-item > input[type="checkbox"][disabled]'
    )
    .forEach(input => {
      if (input.hasAttribute('aria-label')) {
        return;
      }
      const text = input.parentElement?.textContent?.trim().slice(0, 120);
      if (text) {
        input.setAttribute('aria-label', text);
      }
    });
}
