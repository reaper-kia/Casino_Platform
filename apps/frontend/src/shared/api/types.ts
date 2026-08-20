// API DTO — точно повторяют JSON-контракт Gateway (snake_case)

export type GameType = 'crash' | 'roulette' | 'dice_duel';

export type RoomVisibility = 'public' | 'private';

export type RoomStatus = 'open' | 'closed' | 'in_progress';

export interface RoomSummaryDto {
  id: string;
  name: string;
  game_type: GameType;
  visibility: RoomVisibility;
  status: RoomStatus;
  participants_count: number;
  capacity: number;
  min_bet: number;
  max_bet: number;
  created_at: string;
}

export interface RoomsResponseDto {
  rooms: RoomSummaryDto[];
  next_cursor?: string;
  total: number;
}

export interface ApiErrorDto {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}