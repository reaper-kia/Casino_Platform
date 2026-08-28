import { Link, useParams } from 'react-router-dom';
import { Card } from '../shared/ui/Card';
import { StatusBadge } from '../shared/ui/StatusBadge';
import { Button } from '../shared/ui/Button';
import { Spinner } from '../shared/ui/Spinner';
import { ErrorState } from '../shared/ui/ErrorState';
import { EmptyState } from '../shared/ui/EmptyState';
import { useRoomSnapshot } from '../features/room/hooks/useRoomSnapshot';
import { ApiError } from '../shared/api/client';

export function RoomPage() {
  const { roomId } = useParams<{ roomId: string }>();
  const { data: room, isLoading, isError, error, refetch } = useRoomSnapshot(roomId);

  if (isLoading) {
    return (
      <div>
        <h1 className="text-3xl font-bold text-text-primary mb-6">Комната</h1>
        <Spinner size="lg" />
      </div>
    );
  }

  if (isError) {
    const isNotFound = error instanceof ApiError && error.status === 404;

    if (isNotFound) {
      return (
        <div className="text-center py-16">
          <h1 className="text-6xl font-bold text-text-primary mb-4">404</h1>
          <p className="text-xl text-text-secondary mb-2">Комната не найдена</p>
          <p className="text-text-secondary mb-8">
            Возможно, она была закрыта или удалена.
          </p>
          <Link to="/casino">
            <Button>Вернуться в лобби</Button>
          </Link>
        </div>
      );
    }

    return (
      <div>
        <h1 className="text-3xl font-bold text-text-primary mb-6">Комната</h1>
        <ErrorState
          title="Ошибка загрузки"
          message={error instanceof Error ? error.message : 'Не удалось загрузить комнату'}
          onRetry={refetch}
        />
      </div>
    );
  }

  if (!room) {
    return null;
  }

  const statusBadge = (
    <StatusBadge
      status={
        room.status === 'open' ? 'success' : room.status === 'closed' ? 'error' : 'warning'
      }
    >
      {room.status}
    </StatusBadge>
  );

  return (
    <div>
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
        <div>
          <h1 className="text-3xl font-bold text-text-primary mb-2">{room.name}</h1>
          <p className="text-text-secondary capitalize">
            {room.gameType.replace('_', ' ')}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {statusBadge}
          {room.visibility === 'private' && (
            <StatusBadge status="info">Private</StatusBadge>
          )}
          {room.isSystem && <StatusBadge status="warning">System</StatusBadge>}
        </div>
      </div>

      {/* Info card */}
      <Card className="mb-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <div className="text-text-secondary mb-1">Игроки</div>
            <div className="text-text-primary font-semibold text-lg">
              {room.participantsCount} / {room.capacity}
            </div>
          </div>
          <div>
            <div className="text-text-secondary mb-1">Revision</div>
            <div className="text-text-primary font-semibold text-lg">{room.revision}</div>
          </div>
          <div>
            <div className="text-text-secondary mb-1">Создана</div>
            <div className="text-text-primary font-mono text-sm">
              {new Date(room.createdAt).toLocaleString()}
            </div>
          </div>
          <div>
            <div className="text-text-secondary mb-1">Обновлена</div>
            <div className="text-text-primary font-mono text-sm">
              {new Date(room.updatedAt).toLocaleString()}
            </div>
          </div>
        </div>
      </Card>

      {/* Participants */}
      <h2 className="text-xl font-semibold text-text-primary mb-4">Участники</h2>

      {room.participants.length === 0 ? (
        <EmptyState
          title="Участников нет"
          message="В этой комнате пока никого нет."
        />
      ) : (
        <div className="bg-surface border border-border rounded-xl overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border text-left text-text-secondary text-sm">
                <th className="px-4 py-3 font-medium">Seat</th>
                <th className="px-4 py-3 font-medium">Ник</th>
                <th className="px-4 py-3 font-medium">ID игрока</th>
                <th className="px-4 py-3 font-medium">Статус</th>
              </tr>
            </thead>
            <tbody>
              {room.participants.map((p) => (
                <tr key={p.player.playerId} className="border-b border-border last:border-0">
                  <td className="px-4 py-3 text-text-primary">{p.seat}</td>
                  <td className="px-4 py-3 text-text-primary font-medium">
                    {p.player.nickname}
                  </td>
                  <td className="px-4 py-3 text-text-secondary font-mono text-sm">
                    {p.player.playerId}
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge
                      status={
                        p.connectionStatus === 'online'
                          ? 'success'
                          : p.connectionStatus === 'idle'
                          ? 'warning'
                          : 'error'
                      }
                    >
                      {p.connectionStatus}
                    </StatusBadge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="mt-6">
        <Link to="/casino">
          <Button variant="secondary">← Назад в лобби</Button>
        </Link>
      </div>
    </div>
  );
}