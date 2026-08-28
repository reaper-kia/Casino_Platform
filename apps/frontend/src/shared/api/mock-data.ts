import type { ParticipantDto, RoomSnapshotDto, RoomSummaryDto } from './types';

export const mockRooms: RoomSummaryDto[] = [
  {
    room_id: 'room-1',
    name: 'Crash VIP',
    game_type: 'crash',
    visibility: 'public',
    status: 'open',
    participants_count: 3,
    capacity: 100,
    revision: 3,
    owner_player_id: null,
    is_system: false,
    created_at: '2026-08-21T10:00:00Z',
    updated_at: '2026-08-22T09:00:00Z',
    closed_at: null,
  },
  {
    room_id: 'room-2',
    name: 'Roulette Classic',
    game_type: 'roulette',
    visibility: 'public',
    status: 'open',
    participants_count: 2,
    capacity: 50,
    revision: 1,
    owner_player_id: null,
    is_system: false,
    created_at: '2026-08-21T09:30:00Z',
    updated_at: '2026-08-21T09:30:00Z',
    closed_at: null,
  },
  {
    room_id: 'room-3',
    name: 'Dice Duel Pro',
    game_type: 'dice_duel',
    visibility: 'public',
    status: 'closed',
    participants_count: 0,
    capacity: 30,
    revision: 7,
    owner_player_id: 'player-42',
    is_system: false,
    created_at: '2026-08-21T08:00:00Z',
    updated_at: '2026-08-22T08:00:00Z',
    closed_at: '2026-08-22T08:00:00Z',
  },
  {
    room_id: 'room-4',
    name: 'Private Crash',
    game_type: 'crash',
    visibility: 'private',
    status: 'open',
    participants_count: 1,
    capacity: 20,
    revision: 2,
    owner_player_id: 'player-7',
    is_system: false,
    created_at: '2026-08-21T11:00:00Z',
    updated_at: '2026-08-22T10:00:00Z',
    closed_at: null,
  },
  {
    room_id: 'room-5',
    name: 'Roulette Tournament',
    game_type: 'roulette',
    visibility: 'public',
    status: 'archived',
    participants_count: 0,
    capacity: 50,
    revision: 12,
    owner_player_id: null,
    is_system: true,
    created_at: '2026-08-20T07:00:00Z',
    updated_at: '2026-08-21T18:00:00Z',
    closed_at: '2026-08-21T18:00:00Z',
  },
  {
    room_id: 'room-6',
    name: 'Private Dice Club',
    game_type: 'dice_duel',
    visibility: 'private',
    status: 'closed',
    participants_count: 0,
    capacity: 15,
    revision: 4,
    owner_player_id: 'player-99',
    is_system: false,
    created_at: '2026-08-20T06:00:00Z',
    updated_at: '2026-08-21T12:00:00Z',
    closed_at: '2026-08-21T12:00:00Z',
  },
];

const mockParticipantsByRoom: Record<string, ParticipantDto[]> = {
  'room-1': [
    {
      seat: 1,
      connection_status: 'online',
      player: { player_id: 'player-7', nickname: 'Alice', avatar_url: null },
    },
    {
      seat: 2,
      connection_status: 'idle',
      player: { player_id: 'player-42', nickname: 'Bob', avatar_url: null },
    },
    {
      seat: 3,
      connection_status: 'online',
      player: { player_id: 'player-99', nickname: 'Charlie', avatar_url: null },
    },
  ],
  'room-2': [
    {
      seat: 1,
      connection_status: 'online',
      player: { player_id: 'player-11', nickname: 'Dana', avatar_url: null },
    },
    {
      seat: 5,
      connection_status: 'disconnected',
      player: { player_id: 'player-22', nickname: 'Eve', avatar_url: null },
    },
  ],
  'room-4': [
    {
      seat: 1,
      connection_status: 'online',
      player: { player_id: 'player-7', nickname: 'Owner', avatar_url: null },
    },
  ],
  // room-3, room-5, room-6 — закрытые/архивированные, список пустой
};

/**
 * Mock snapshot для конкретной комнаты.
 * Возвращает null, если комнаты нет в каталоге.
 */
export function getMockSnapshot(roomId: string): RoomSnapshotDto | null {
  const room = mockRooms.find((r) => r.room_id === roomId);
  if (!room) return null;
  return {
    ...room,
    participants: mockParticipantsByRoom[roomId] ?? [],
  };
}