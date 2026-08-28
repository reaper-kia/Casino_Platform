import type {
  GameType,
  RoomStatus,
  RoomSummaryDto,
  RoomVisibility,
} from './types';

// UI-модель комнаты: удобные для React имена (camelCase).
// НЕ смешиваем с DTO.
export interface RoomSummary {
  roomId: string;
  name: string;
  gameType: GameType;
  visibility: RoomVisibility;
  status: RoomStatus;
  participantsCount: number;
  capacity: number;
  revision: number;
  ownerPlayerId: string | null;
  isSystem: boolean;
  createdAt: string;
  updatedAt: string;
  closedAt: string | null;
}

// Mapper: RoomSummaryDto -> RoomSummary
export function mapRoomSummary(dto: RoomSummaryDto): RoomSummary {
  return {
    roomId: dto.room_id,
    name: dto.name,
    gameType: dto.game_type,
    visibility: dto.visibility,
    status: dto.status,
    participantsCount: dto.participants_count,
    capacity: dto.capacity,
    revision: dto.revision,
    ownerPlayerId: dto.owner_player_id,
    isSystem: dto.is_system,
    createdAt: dto.created_at,
    updatedAt: dto.updated_at,
    closedAt: dto.closed_at,
  };
}