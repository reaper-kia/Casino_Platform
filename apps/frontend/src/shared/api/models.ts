import type { RoomSummaryDto, GameType, RoomVisibility, RoomStatus } from './types';

// UI модель с удобными именами (camelCase)
export interface RoomSummary {
  id: string;
  name: string;
  gameType: GameType;
  visibility: RoomVisibility;
  status: RoomStatus;
  participantsCount: number;
  capacity: number;
  minBet: number;
  maxBet: number;
  createdAt: Date;
}

// Mapper: API DTO → UI модель
export function mapRoomSummary(dto: RoomSummaryDto): RoomSummary {
  return {
    id: dto.id,
    name: dto.name,
    gameType: dto.game_type,
    visibility: dto.visibility,
    status: dto.status,
    participantsCount: dto.participants_count,
    capacity: dto.capacity,
    minBet: dto.min_bet,
    maxBet: dto.max_bet,
    createdAt: new Date(dto.created_at),
  };
}