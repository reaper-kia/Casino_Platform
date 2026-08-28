import { useInfiniteQuery } from '@tanstack/react-query';
import { mapRoomSummary } from '../../../shared/api/models';
import { fetchRooms, type RoomsFilters } from '../../../shared/api/rooms-api';

// pageParam — opaque cursor: фронтенд не интерпретирует его содержимое,
// а только передаёт серверу и получает обратно через next_cursor.
type PageParam = string | null;

export function useRooms(filters: RoomsFilters = {}) {
  return useInfiniteQuery({
    // Стабильный query key, включающий фильтры
    queryKey: ['rooms', filters],

    // Стартовый курсор — null (первая страница)
    initialPageParam: null as PageParam,

    queryFn: ({ pageParam, signal }) =>
      fetchRooms({ ...filters, cursor: pageParam ?? undefined, signal }),

    // Курсор следующей страницы из ответа сервера;
    // undefined означает «страниц больше нет»
    getNextPageParam: (lastPage) => lastPage.next_cursor ?? undefined,

    // Новые страницы добавляются к уже загруженным
    select: (data) => ({
      rooms: data.pages.flatMap((page) => page.items).map(mapRoomSummary),
    }),
  });
}