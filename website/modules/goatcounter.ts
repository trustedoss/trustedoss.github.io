import type {Location} from 'history';

declare global {
  interface Window {
    goatcounter?: {
      count: (vars?: {path?: string; title?: string; event?: boolean}) => void;
    };
  }
}

// 첫 페이지 로드는 count.js가 자동 집계하므로, 여기서는 SPA 라우트 전환만 집계한다.
// count.js는 localhost 방문을 기본으로 무시하므로 로컬 개발은 집계되지 않는다.
export function onRouteDidUpdate({
  location,
  previousLocation,
}: {
  location: Location;
  previousLocation: Location | null;
}): void {
  if (!previousLocation) {
    return;
  }
  if (
    location.pathname === previousLocation.pathname &&
    location.search === previousLocation.search
  ) {
    return;
  }
  // 라우트 전환 직후에는 document.title이 아직 이전 페이지 값이라
  // 제목 갱신 이후로 전송을 미룬다 (공식 gtag 플러그인과 같은 방식)
  setTimeout(() => {
    window.goatcounter?.count?.({
      path: location.pathname + location.search,
      title: document.title,
    });
  }, 50);
}
