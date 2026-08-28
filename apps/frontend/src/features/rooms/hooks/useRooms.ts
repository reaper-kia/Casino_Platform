import { useInfiniteQuery } from '@tanstack/react-query';
import { mapRoomSummary } from '../../../shared/api/models';
import { fetchRooms, type RoomsFilters } from '../../../shared/api/rooms-api';

export function useRooms(filters: RoomsFilters = {}) {
  return useInfiniteQuery({
    queryKey: ['rooms', filters],
    initialPageParam: null as string | null,
    queryFn: ({ pageParam, signal }) =>
      fetchRooms({ ...filters, cursor: pageParam ?? undefined, signal }),
    getNextPageParam: (lastPage) => lastPage.next_cursor ?? undefined,
    select: (data) => ({
      rooms: data.pages.flatMap((page) => page.items).map(mapRoomSummary),
    }),
  });
}