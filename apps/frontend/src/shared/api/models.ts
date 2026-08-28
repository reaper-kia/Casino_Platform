import type {
  ConnectionStatus,
  GameType,
  ParticipantDto,
  PlayerDto,
  RoomSnapshotDto,
  RoomStatus,
  RoomSummaryDto,
  RoomVisibility,
} from './types';

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

export interface Player {
  playerId: string;
  nickname: string;
  avatarUrl: string | null;
}

export interface Participant {
  seat: number;
  connectionStatus: ConnectionStatus;
  player: Player;
}

export interface RoomSnapshot {
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
  participants: Participant[];
}

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

export function mapPlayer(dto: PlayerDto): Player {
  return {
    playerId: dto.player_id,
    nickname: dto.nickname,
    avatarUrl: dto.avatar_url,
  };
}

export function mapParticipant(dto: ParticipantDto): Participant {
  return {
    seat: dto.seat,
    connectionStatus: dto.connection_status,
    player: mapPlayer(dto.player),
  };
}

export function mapRoomSnapshot(dto: RoomSnapshotDto): RoomSnapshot {
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
    participants: dto.participants.map(mapParticipant),
  };
}