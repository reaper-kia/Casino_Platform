export type ApiMode = 'mock' | 'real';

const DEFAULT_API_BASE_URL = 'http://localhost:8000/api/v1';
const DEFAULT_WS_BASE_URL = 'ws://localhost:8000/ws/v1';

function resolveApiMode(): ApiMode {
  const raw: string | undefined = import.meta.env.VITE_API_MODE;

  if (raw === 'mock' || raw === 'real') {
    return raw;
  }

  // Без переменной НЕ уходим в mock: production с забытым env
  // должен ходить в реальный Gateway.
  if (raw === undefined || raw === '') {
    return 'real';
  }

  throw new Error(
    `[config] Невалидное значение VITE_API_MODE="${raw}". Допустимо только "mock" или "real".`,
  );
}

export const env = {
  get apiBaseUrl(): string {
    return import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL;
  },
  get wsBaseUrl(): string {
    return import.meta.env.VITE_WS_BASE_URL || DEFAULT_WS_BASE_URL;
  },
  get apiMode(): ApiMode {
    return resolveApiMode();
  },
};