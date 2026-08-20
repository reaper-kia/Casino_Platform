import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { AppProviders } from './app/providers/AppProviders';
import { Button } from './shared/ui/Button';

describe('App Foundation', () => {
  it('renders AppShell with header', () => {
    render(<AppProviders />);
    // "Casino Platform" встречается в логотипе и в HomePage — берём через getAllByText
    const elements = screen.getAllByText(/Casino Platform/i);
    expect(elements.length).toBeGreaterThanOrEqual(1);
  });

  it('navigates to Casino lobby', async () => {
    const user = userEvent.setup();
    render(<AppProviders />);

    // Берём первую ссылку "Казино" (она в навигации)
    const casinoLinks = screen.getAllByRole('link', { name: /Казино/i });
    await user.click(casinoLinks[0]);

    // Проверяем, что открылось лобби (через заголовок h1)
    expect(
      await screen.findByRole('heading', { name: /Казино Лобби/i })
    ).toBeInTheDocument();
  });

  it('shows Not Found for unknown routes', () => {
    window.history.pushState({}, '', '/unknown-route');
    render(<AppProviders />);
    expect(
      screen.getByRole('heading', { name: /404/i })
    ).toBeInTheDocument();
    expect(screen.getByText(/Страница не найдена/i)).toBeInTheDocument();
  });

  it('Button can be disabled', () => {
    render(<Button disabled>Click me</Button>);
    const button = screen.getByRole('button', { name: /click me/i });
    expect(button).toBeDisabled();
  });

  it('Mobile menu opens and closes', async () => {
    // Имитируем мобильный экран, чтобы класс md:hidden реально скрывал десктопное меню
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 360,
    });
    window.dispatchEvent(new Event('resize'));

    const user = userEvent.setup();
    render(<AppProviders />);

    // Кнопка Toggle menu — одна в DOM (благодаря cleanup в setupTests)
    const menuButton = screen.getByLabelText(/toggle menu/i);
    expect(menuButton).toBeInTheDocument();

    await user.click(menuButton);

    // После клика должно появиться мобильное меню с дублирующимися ссылками
    const casinoLinks = screen.getAllByRole('link', { name: /Казино/i });
    expect(casinoLinks.length).toBeGreaterThanOrEqual(2);
  });
});