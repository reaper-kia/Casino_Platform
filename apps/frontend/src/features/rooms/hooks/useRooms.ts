import { useQuery } from '@tanstack/react-query';
import { fetchRooms, type RoomsFilters } from '../../../shared/api/rooms-api';
import { mapRoomSummary } from '../../../shared/api/models';

export function useRooms(filters: RoomsFilters = {}) {
  return useQuery({
    queryKey: ['rooms', filters],
    queryFn: ({ signal }) => fetchRooms({ ...filters, signal }),
    select: (data) => ({
      rooms: data.rooms.map(mapRoomSummary),
      nextCursor: data.next_cursor,
      total: data.total,
    }),
  });
}