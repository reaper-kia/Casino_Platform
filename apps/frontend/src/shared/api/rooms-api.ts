import { env } from '../config/env';
import { api } from './client';
import { mockRooms } from './mock-data';
import type {
  GameType,
  RoomStatus,
  RoomVisibility,
  RoomsResponseDto,
} from './types';

export const DEFAULT_PAGE_SIZE = 4;

export interface RoomsFilters {
  gameType?: GameType;
  visibility?: RoomVisibility;
  status?: RoomStatus;
  limit?: number;
}

export interface FetchRoomsParams extends RoomsFilters {
  cursor?: string;
  signal?: AbortSignal;
}

export async function fetchRooms(
  params: FetchRoomsParams = {},
): Promise<RoomsResponseDto> {
  if (env.apiMode === 'mock') {
    return fetchRoomsMock(params);
  }
  return fetchRoomsReal(params);
}

function parseCursor(cursor: string | undefined): number {
  if (!cursor) return 0;
  const parsed = Number.parseInt(cursor, 10);
  return Number.isFinite(parsed) && parsed >= 0 ? parsed : 0;
}

async function fetchRoomsMock(
  params: FetchRoomsParams,
): Promise<RoomsResponseDto> {
  // Имитация сетевой задержки, чтобы loading-состояния были видимыми
  await new Promise((resolve) => setTimeout(resolve, 300));

  const filtered = mockRooms.filter((room) => {
    if (params.gameType && room.game_type !== params.gameType) return false;
    if (params.visibility && room.visibility !== params.visibility) return false;
    if (params.status && room.status !== params.status) return false;
    return true;
  });

  const limit = params.limit ?? DEFAULT_PAGE_SIZE;
  const offset = parseCursor(params.cursor);
  const items = filtered.slice(offset, offset + limit);
  const nextOffset = offset + limit;

  return {
    items,
    next_cursor: nextOffset < filtered.length ? String(nextOffset) : null,
  };
}

async function fetchRoomsReal(
  params: FetchRoomsParams,
): Promise<RoomsResponseDto> {
  const searchParams = new URLSearchParams();
  if (params.gameType) searchParams.set('game_type', params.gameType);
  if (params.visibility) searchParams.set('visibility', params.visibility);
  if (params.status) searchParams.set('status', params.status);
  if (params.limit) searchParams.set('limit', String(params.limit));
  if (params.cursor) searchParams.set('cursor', params.cursor);

  const query = searchParams.toString();
  return api.get<RoomsResponseDto>(`/casino/rooms${query ? `?${query}` : ''}`, {
    signal: params.signal,
  });
}