import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Card } from '../shared/ui/Card';
import { StatusBadge } from '../shared/ui/StatusBadge';
import { Button } from '../shared/ui/Button';
import { Spinner } from '../shared/ui/Spinner';
import { ErrorState } from '../shared/ui/ErrorState';
import { EmptyState } from '../shared/ui/EmptyState';
import { useRooms } from '../features/rooms/hooks/useRooms';
import type { GameType, RoomVisibility, RoomStatus } from '../shared/api/types';

export function CasinoLobbyPage() {
  const [gameType, setGameType] = useState<GameType | ''>('');
  const [visibility, setVisibility] = useState<RoomVisibility | ''>('');
  const [status, setStatus] = useState<RoomStatus | ''>('');

  const filters = {
    gameType: gameType || undefined,
    visibility: visibility || undefined,
    status: status || undefined,
  };

  const {
    data,
    isLoading,
    isError,
    error,
    refetch,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useRooms(filters);

  const resetFilters = () => {
    setGameType('');
    setVisibility('');
    setStatus('');
  };

  const rooms = data?.rooms ?? [];

  return (
    <div>
      <h1 className="text-3xl font-bold text-text-primary mb-6">Казино Лобби</h1>

      {/* Фильтры — видны всегда */}
      <div className="bg-surface border border-border rounded-xl p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label htmlFor="game-type-filter" className="block text-sm font-medium text-text-secondary mb-1.5">
              Тип игры
            </label>
            <select
              id="game-type-filter"
              value={gameType}
              onChange={(e) => setGameType(e.target.value as GameType | '')}
              className="w-full px-4 py-2.5 bg-surface-elevated border border-border rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-focus-ring"
            >
              <option value="">Все игры</option>
              <option value="crash">Crash</option>
              <option value="roulette">Roulette</option>
              <option value="dice_duel">Dice Duel</option>
            </select>
          </div>

          <div>
            <label htmlFor="visibility-filter" className="block text-sm font-medium text-text-secondary mb-1.5">
              Видимость
            </label>
            <select
              id="visibility-filter"
              value={visibility}
              onChange={(e) => setVisibility(e.target.value as RoomVisibility | '')}
              className="w-full px-4 py-2.5 bg-surface-elevated border border-border rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-focus-ring"
            >
              <option value="">Все</option>
              <option value="public">Public</option>
              <option value="private">Private</option>
            </select>
          </div>

          <div>
            <label htmlFor="status-filter" className="block text-sm font-medium text-text-secondary mb-1.5">
              Статус
            </label>
            <select
              id="status-filter"
              value={status}
              onChange={(e) => setStatus(e.target.value as RoomStatus | '')}
              className="w-full px-4 py-2.5 bg-surface-elevated border border-border rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-focus-ring"
            >
              <option value="">Все</option>
              <option value="open">Open</option>
              <option value="closed">Closed</option>
              <option value="archived">Archived</option>
            </select>
          </div>

          <div className="flex items-end">
            <Button onClick={resetFilters} variant="secondary" className="w-full">
              Сбросить
            </Button>
          </div>
        </div>
      </div>

      {/* Область контента: loading / error / empty / success */}
      {isLoading ? (
        <Spinner size="lg" />
      ) : isError ? (
        <ErrorState
          title="Ошибка загрузки"
          message={error instanceof Error ? error.message : 'Не удалось загрузить комнаты'}
          onRetry={refetch}
        />
      ) : rooms.length === 0 ? (
        <EmptyState
          title="Комнаты не найдены"
          message="Попробуйте изменить фильтры или сбросить их"
          action={{
            label: 'Сбросить фильтры',
            onClick: resetFilters,
          }}
        />
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
            {rooms.map((room) => (
              <Link key={room.roomId} to={`/casino/rooms/${room.roomId}`}>
                <Card className="hover:bg-surface-elevated transition-colors cursor-pointer h-full">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-semibold text-text-primary mb-1">
                        {room.name}
                      </h3>
                      <p className="text-sm text-text-secondary capitalize">
                        {room.gameType.replace('_', ' ')}
                      </p>
                    </div>
                    <div className="flex flex-col items-end gap-2">
                      <StatusBadge
                        status={
                          room.status === 'open'
                            ? 'success'
                            : room.status === 'closed'
                            ? 'error'
                            : 'warning'
                        }
                      >
                        {room.status}
                      </StatusBadge>
                      {room.visibility === 'private' && (
                        <StatusBadge status="info">Private</StatusBadge>
                      )}
                    </div>
                  </div>

                  <div className="space-y-2 text-sm text-text-secondary">
                    <div className="flex justify-between">
                      <span>Игроки:</span>
                      <span className="text-text-primary font-medium">
                        {room.participantsCount} / {room.capacity}
                      </span>
                    </div>
                  </div>
                </Card>
              </Link>
            ))}
          </div>

          {hasNextPage && (
            <div className="flex justify-center">
              <Button
                variant="secondary"
                onClick={() => fetchNextPage()}
                loading={isFetchingNextPage}
                disabled={isFetchingNextPage}
              >
                Загрузить ещё
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
}