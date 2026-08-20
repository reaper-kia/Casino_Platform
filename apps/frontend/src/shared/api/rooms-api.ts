import { env } from '../config/env';
import { api } from './client';
import { mockRooms } from './mock-data';
import type { RoomsResponseDto, GameType, RoomVisibility, RoomStatus } from './types';

export interface RoomsFilters {
  gameType?: GameType;
  visibility?: RoomVisibility;
  status?: RoomStatus;
  limit?: number;
  cursor?: string;
}

export interface FetchRoomsParams extends RoomsFilters {
  signal?: AbortSignal;
}

export async function fetchRooms(
  params: FetchRoomsParams = {},
): Promise<RoomsResponseDto> {
  // Mock режим включается явно через VITE_API_MODE=mock
  if (env.apiMode === 'mock') {
    await new Promise((resolve) => setTimeout(resolve, 500)); // Имитация задержки
    
    let filtered = [...mockRooms];
    
    if (params.gameType) {
      filtered = filtered.filter((r) => r.game_type === params.gameType);
    }
    if (params.visibility) {
      filtered = filtered.filter((r) => r.visibility === params.visibility);
    }
    if (params.status) {
      filtered = filtered.filter((r) => r.status === params.status);
    }
    
    const limit = params.limit ?? 10;
    const paginated = filtered.slice(0, limit);
    
    return {
      rooms: paginated,
      total: filtered.length,
      next_cursor: filtered.length > limit ? 'cursor-next' : undefined,
    };
  }

  // Реальный API
  const searchParams = new URLSearchParams();
  if (params.gameType) searchParams.set('game_type', params.gameType);
  if (params.visibility) searchParams.set('visibility', params.visibility);
  if (params.status) searchParams.set('status', params.status);
  if (params.limit) searchParams.set('limit', String(params.limit));
  if (params.cursor) searchParams.set('cursor', params.cursor);

  const query = searchParams.toString();
  const path = `/casino/rooms${query ? `?${query}` : ''}`;
  
  return api.get<RoomsResponseDto>(path, { signal: params.signal });
}