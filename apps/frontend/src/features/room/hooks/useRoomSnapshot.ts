import { useQuery } from '@tanstack/react-query';
import { ApiError } from '../../../shared/api/client';
import { fetchRoomSnapshot } from '../../../shared/api/rooms-api';
import { mapRoomSnapshot } from '../../../shared/api/models';

export function useRoomSnapshot(roomId: string | undefined) {
  return useQuery({
    queryKey: ['room-snapshot', roomId],
    enabled: Boolean(roomId),
    queryFn: ({ signal }) => fetchRoomSnapshot({ roomId: roomId!, signal }),
    select: mapRoomSnapshot,
    // 404 — финальное состояние NotFound, ретраить не нужно
    retry: (count, error) => {
      if (error instanceof ApiError && error.status === 404) return false;
      return count < 2;
    },
  });
}