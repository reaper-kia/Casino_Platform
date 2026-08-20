import { Link } from 'react-router-dom';
import { Card } from '../shared/ui/Card';
import { StatusBadge } from '../shared/ui/StatusBadge';

const rooms = [
  { id: '1', name: 'VIP Roulette', players: 12, status: 'active' as const },
  { id: '2', name: 'Blackjack Pro', players: 8, status: 'active' as const },
  { id: '3', name: 'Poker Classic', players: 0, status: 'waiting' as const },
];

export function CasinoLobbyPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-text-primary mb-6">Казино Лобби</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {rooms.map((room) => (
          <Link key={room.id} to={`/casino/rooms/${room.id}`}>
            <Card className="hover:bg-surface-elevated transition-colors cursor-pointer">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-semibold text-text-primary">{room.name}</h3>
                <StatusBadge status={room.status === 'active' ? 'success' : 'warning'}>
                  {room.status === 'active' ? 'Активна' : 'Ожидание'}
                </StatusBadge>
              </div>
              <p className="text-text-secondary">Игроков: {room.players}</p>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}