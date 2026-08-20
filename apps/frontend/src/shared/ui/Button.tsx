import type { ReactNode } from 'react';

export function Button({ children }: { children: ReactNode }) {
  return (
    <button className="mt-4 rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600">
      {children}
    </button>
  );
}