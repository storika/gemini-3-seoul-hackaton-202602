import { useRef, useCallback } from "react";

export function useDebounce<T extends (...args: unknown[]) => void>(
  fn: T,
  delay: number
): T {
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  return useCallback(
    (...args: Parameters<T>) => {
      if (timer.current) clearTimeout(timer.current);
      timer.current = setTimeout(() => fn(...args), delay);
    },
    [fn, delay]
  ) as T;
}
