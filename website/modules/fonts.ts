/**
 * 셀프호스트 Roboto (Apache-2.0). Material/Gemini docs 타이포.
 * 라틴은 Roboto, 한글은 Pretendard Variable (SIL OFL, 유니코드 레인지별
 * dynamic subset이라 초기 로드가 작다)로 폴백. OS별 렌더링 차이를 없앤다.
 * 키릴·그리스·베트남어 서브셋은 이 사이트에서 쓰지 않아 latin 서브셋만 불러온다
 * (전체 서브셋을 불러오면 CSS에 base64 글꼴 340KB가 모든 페이지에 실린다).
 * 제목 굵기 600을 쓰므로 600을 불러오고, 쓰지 않는 700은 불러오지 않는다.
 */
import '@fontsource/roboto/latin-400.css';
import '@fontsource/roboto/latin-500.css';
import '@fontsource/roboto/latin-600.css';
import '@fontsource/roboto-mono/latin-400.css';
import 'pretendard/dist/web/variable/pretendardvariable-dynamic-subset.css';
