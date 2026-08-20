import { useParams } from 'react-router-dom';
import { Card } from '../shared/ui/Card';
import { StatusBadge } from '../shared/ui/StatusBadge';

export function RoomPage() {
  const { roomId } = useParams<{ roomId: string }>();

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-text-primary">Комната #{roomId}</h1>
        <StatusBadge status="success">В игре</StatusBadge>
      </div>
      <Card>
        <div className="text-center py-12">
          <p className="text-text-secondary mb-4">Здесь будет игровая логика</p>
          <p className="text-2xl font-mono text-accent">Комната {roomId}</p>
        </div>
      </Card>
    </div>
  );
}