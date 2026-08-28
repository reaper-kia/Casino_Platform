// API DTO — полностью повторяют JSON-контракт Gateway (snake_case)

export type GameType = 'crash' | 'roulette' | 'dice_duel';

export type RoomVisibility = 'public' | 'private';

export type RoomStatus = 'open' | 'closed' | 'archived';

export type ConnectionStatus = 'online' | 'disconnected' | 'idle';

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

export interface PlayerDto {
  player_id: string;
  nickname: string;
  avatar_url: string | null;
}

export interface ParticipantDto {
  seat: number;
  connection_status: ConnectionStatus;
  player: PlayerDto;
}

// Snapshot комнаты (docs/gateway-api.md, раздел 7.3)
export interface RoomSnapshotDto {
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
  participants: ParticipantDto[];
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

export interface ApiErrorResponseDto {
  error: ApiErrorDto;
}