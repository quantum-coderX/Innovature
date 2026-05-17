import { useEffect, useRef } from "react";

/**
 * Attaches an IntersectionObserver to `ref`.
 * Calls `onIntersect` when the element enters the viewport.
 */
export function useSentinel(onIntersect, { enabled = true } = {}) {
  const ref = useRef(null);

  useEffect(() => {
    if (!enabled) return;
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) onIntersect();
      },
      { threshold: 0.1 }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [onIntersect, enabled]);

  return ref;
}
