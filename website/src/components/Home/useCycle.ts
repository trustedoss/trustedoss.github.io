/**
 * 카드 묶음을 한 장씩 돌아가며 강조하는 훅.
 * 화면에 보일 때만 순환하고, 마우스나 키보드 포커스가 올라간 카드가 있으면
 * 그 카드가 강조를 가져가며 순환은 멈춘다. 모션 감소 설정에서는 순환 없이
 * 첫 카드만 강조한다.
 */

import {useEffect, useRef, useState} from 'react';

const CYCLE_MS = 4000;

export default function useCycle<T extends HTMLElement>(count: number) {
  const [index, setIndex] = useState(0);
  const [pinned, setPinned] = useState<number | null>(null);
  const [visible, setVisible] = useState(false);
  const [reduced, setReduced] = useState(false);
  const ref = useRef<T>(null);

  useEffect(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    setReduced(mq.matches);
    const onChange = () => setReduced(mq.matches);
    mq.addEventListener('change', onChange);
    return () => mq.removeEventListener('change', onChange);
  }, []);

  useEffect(() => {
    const el = ref.current;
    if (!el || typeof IntersectionObserver === 'undefined') {
      return undefined;
    }
    const io = new IntersectionObserver(([e]) => setVisible(e.isIntersecting), {
      threshold: 0.3,
    });
    io.observe(el);
    return () => io.disconnect();
  }, []);

  useEffect(() => {
    if (!visible || pinned !== null || reduced) {
      return undefined;
    }
    const id = window.setInterval(() => {
      if (!document.hidden) {
        setIndex(i => (i + 1) % count);
      }
    }, CYCLE_MS);
    return () => window.clearInterval(id);
  }, [visible, pinned, reduced, count]);

  return {
    ref,
    current: pinned ?? index,
    enter: (i: number) => () => {
      setPinned(i);
      setIndex(i);
    },
    leave: () => setPinned(null),
  };
}
