import { Link } from 'react-router-dom';
import { Button } from '../shared/ui/Button';
import { Input } from '../shared/ui/Input';
import { Card } from '../shared/ui/Card';

export function LoginPage() {
  return (
    <div className="max-w-md mx-auto py-12">
      <Card>
        <h1 className="text-2xl font-bold text-text-primary mb-6 text-center">Вход</h1>
        <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
          <Input label="Email" type="email" placeholder="your@email.com" />
          <Input label="Пароль" type="password" placeholder="••••••••" />
          <Button type="submit" className="w-full">
            Войти
          </Button>
        </form>
        <p className="mt-4 text-center text-text-secondary">
          Нет аккаунта?{' '}
          <Link to="/register" className="text-accent hover:underline">
            Зарегистрируйтесь
          </Link>
        </p>
      </Card>
    </div>
  );
}