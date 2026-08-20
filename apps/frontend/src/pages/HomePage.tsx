import { Link } from 'react-router-dom';
import { Button } from '../shared/ui/Button';
import { Card } from '../shared/ui/Card';

export function HomePage() {
  return (
    <div className="space-y-8">
      <div className="text-center py-12">
        <h1 className="text-4xl sm:text-5xl font-bold text-text-primary mb-4">
          Добро пожаловать в Casino Platform
        </h1>
        <p className="text-xl text-text-secondary mb-8">
          Лучшие игры и бонусы ждут вас
        </p>
        <Link to="/casino">
          <Button size="lg">Начать игру</Button>
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <h3 className="text-xl font-semibold text-text-primary mb-2">Слоты</h3>
          <p className="text-text-secondary mb-4">Более 1000 игровых автоматов</p>
        </Card>
        <Card>
          <h3 className="text-xl font-semibold text-text-primary mb-2">Живые игры</h3>
          <p className="text-text-secondary mb-4">Играйте с реальными дилерами</p>
        </Card>
        <Card>
          <h3 className="text-xl font-semibold text-text-primary mb-2">Турниры</h3>
          <p className="text-text-secondary mb-4">Ежедневные соревнования</p>
        </Card>
      </div>
    </div>
  );
}