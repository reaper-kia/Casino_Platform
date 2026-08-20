import { Button } from '../shared/ui/Button';

export function HomePage() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-blue-600">Casino Platform Frontend</h1>
      <p className="mt-4 text-gray-700">Foundation is ready.</p>
      <Button>Click me</Button>
    </div>
  );
}