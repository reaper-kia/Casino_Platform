import { env } from '../config/env';
import type { ApiErrorDto } from './types';

export class ApiError extends Error {
  code: string;
  details?: Record<string, unknown>;
  status?: number;

  constructor(
    code: string,
    message: string,
    details?: Record<string, unknown>,
    status?: number,
  ) {
    super(message);
    this.name = 'ApiError';
    this.code = code;
    this.details = details;
    this.status = status;
  }
}

interface RequestOptions {
  signal?: AbortSignal;
}

async function request<T>(
  path: string,
  options: RequestOptions = {},
): Promise<T> {
  const url = `${env.apiBaseUrl}${path}`;

  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'X-Request-ID': crypto.randomUUID(),
    },
    credentials: 'include',
    signal: options.signal,
  });

  // Корректно обрабатываем пустой ответ
  if (response.status === 204 || response.headers.get('content-length') === '0') {
    return undefined as T;
  }

  if (!response.ok) {
    let error: ApiErrorDto;
    try {
      error = await response.json();
    } catch {
      throw new ApiError(
        'UNKNOWN_ERROR',
        `HTTP ${response.status}`,
        undefined,
        response.status,
      );
    }
    throw new ApiError(error.code, error.message, error.details, response.status);
  }

  return response.json();
}

export const api = {
  get: request,
};