// API DTO — полностью повторяют JSON-контракт Gateway
// (docs/gateway-api.md, раздел 7.1 «Список комнат»).
// Имена полей — snake_case, как отдаёт сервер.

export type GameType = 'crash' | 'roulette' | 'dice_duel';

export type RoomVisibility = 'public' | 'private';

export type RoomStatus = 'open' | 'closed' | 'archived';

export interface RoomSummaryDto {
  room_id: string;
  name: string;
  game_type: GameType;
  visibility: RoomVisibility;
  status: RoomStatus;
  participants_count: number;
  capacity: number;
  revision: number;
  owner_player_id: string | null;
  is_system: boolean;
  created_at: string;
  updated_at: string;
  closed_at: string | null;
}

export interface RoomsResponseDto {
  items: RoomSummaryDto[];
  next_cursor: string | null;
}

export interface ApiErrorDetailDto {
  field: string;
  message: string;
}

export interface ApiErrorDto {
  code: string;
  message: string;
  request_id: string;
  details: ApiErrorDetailDto[];
}

// Корневой формат ошибки Gateway
export interface ApiErrorResponseDto {
  error: ApiErrorDto;
}