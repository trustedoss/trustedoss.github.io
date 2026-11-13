/*
 * 도구 페이지 공통: 사이트 테마 연동과 iframe 높이 맞춤.
 * 사이트(부모 문서)와 같은 출처이므로 부모의 data-theme 값을 직접 읽고 변경을 따라간다.
 * 부모를 읽을 수 없거나 단독으로 열었을 때는 OS 설정(prefers-color-scheme)을 따른다.
 * 색은 각 도구의 :root 와 :root[data-theme="dark"] 토큰으로 정한다.
 */
(function () {
  var root = document.documentElement;
  var mq = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

  function parentTheme() {
    try {
      if (window.parent && window.parent !== window) {
        var t = window.parent.document.documentElement.getAttribute("data-theme");
        if (t === "dark" || t === "light") return t;
      }
    } catch (e) {
      /* 다른 출처이면 읽을 수 없다 */
    }
    return null;
  }

  function apply() {
    var t = parentTheme() || (mq && mq.matches ? "dark" : "light");
    root.setAttribute("data-theme", t);
  }

  apply();
  if (mq && mq.addEventListener) mq.addEventListener("change", apply);
  try {
    if (window.parent && window.parent !== window) {
      new MutationObserver(apply).observe(window.parent.document.documentElement, {
        attributes: true,
        attributeFilter: ["data-theme"],
      });
    }
  } catch (e) {
    /* 무시 */
  }

  // iframe 높이를 내용에 맞춰 안쪽 스크롤이 생기지 않게 한다(같은 출처일 때만).
  var frame = null;
  try {
    frame = window.frameElement;
  } catch (e) {
    frame = null;
  }
  function startFit() {
    var last = 0;
    var fit = function () {
      var h = Math.ceil(document.body.getBoundingClientRect().height + 32);
      if (h > 200 && Math.abs(h - last) > 2) {
        last = h;
        frame.style.height = h + "px";
        frame.removeAttribute("height");
      }
    };
    new ResizeObserver(fit).observe(document.body);
    window.addEventListener("load", fit);
  }
  if (frame && window.ResizeObserver) {
    if (document.body) startFit();
    else document.addEventListener("DOMContentLoaded", startFit);
  }
})();
