import { env } from '../config/env';
import type { ApiErrorResponseDto } from './types';

export class ApiError extends Error {
  code: string;
  requestId?: string;
  details?: unknown[];
  status?: number;

  constructor(
    code: string,
    message: string,
    requestId?: string,
    details?: unknown[],
    status?: number,
  ) {
    super(message);
    this.name = 'ApiError';
    this.code = code;
    this.requestId = requestId;
    this.details = details;
    this.status = status;
  }
}

interface RequestOptions {
  signal?: AbortSignal;
}

function isApiErrorResponse(value: unknown): value is ApiErrorResponseDto {
  if (typeof value !== 'object' || value === null) return false;
  const candidate = (value as { error?: unknown }).error;
  if (typeof candidate !== 'object' || candidate === null) return false;
  const e = candidate as Record<string, unknown>;
  return (
    typeof e.code === 'string' &&
    typeof e.message === 'string' &&
    typeof e.request_id === 'string' &&
    Array.isArray(e.details)
  );
}

async function toApiError(response: Response): Promise<ApiError> {
  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    payload = undefined;
  }

  if (isApiErrorResponse(payload)) {
    const e = payload.error;
    return new ApiError(e.code, e.message, e.request_id, e.details, response.status);
  }

  // Неизвестный или невалидный формат ответа — безопасная общая ошибка
  return new ApiError(
    'UNKNOWN_ERROR',
    'Что-то пошло не так. Попробуйте позже.',
    undefined,
    [],
    response.status,
  );
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
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

  if (!response.ok) {
    throw await toApiError(response);
  }

  // Корректно обрабатываем пустой ответ
  if (response.status === 204) {
    return undefined as T;
  }

  const text = await response.text();
  if (text.trim() === '') {
    return undefined as T;
  }

  return JSON.parse(text) as T;
}

export const api = {
  get: request,
};