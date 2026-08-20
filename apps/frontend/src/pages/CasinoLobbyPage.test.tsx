import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi, beforeEach } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { CasinoLobbyPage } from './CasinoLobbyPage';

const wrapper = ({ children }: { children: React.ReactNode }) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{children}</BrowserRouter>
    </QueryClientProvider>
  );
};

describe('CasinoLobbyPage', () => {
  beforeEach(() => {
    vi.stubEnv('VITE_API_MODE', 'mock');
  });

  it('показывает spinner во время загрузки', () => {
    render(<CasinoLobbyPage />, { wrapper });
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('показывает комнаты после загрузки', async () => {
    render(<CasinoLobbyPage />, { wrapper });
    
    await waitFor(() => {
      expect(screen.getByText('Crash VIP')).toBeInTheDocument();
      expect(screen.getByText('Roulette Classic')).toBeInTheDocument();
    });
  });

  it('фильтр по game_type изменяет список', async () => {
    const user = userEvent.setup();
    render(<CasinoLobbyPage />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText('Crash VIP')).toBeInTheDocument();
    });

    const gameTypeSelect = screen.getByLabelText(/Тип игры/i);
    await user.selectOptions(gameTypeSelect, 'roulette');

    await waitFor(() => {
      expect(screen.queryByText('Crash VIP')).not.toBeInTheDocument();
      expect(screen.getByText('Roulette Classic')).toBeInTheDocument();
    });
  });

  it('показывает EmptyState при пустом результате', async () => {
    const user = userEvent.setup();
    render(<CasinoLobbyPage />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText('Crash VIP')).toBeInTheDocument();
    });

    // Выбираем комбинацию: crash + in_progress. 
    // В mock нет crash-комнат со статусом in_progress → пустой результат.
    const gameTypeSelect = screen.getByLabelText(/Тип игры/i);
    await user.selectOptions(gameTypeSelect, 'crash');

    const statusSelect = screen.getByLabelText(/Статус/i);
    await user.selectOptions(statusSelect, 'in_progress');

    await waitFor(() => {
      expect(screen.getByText(/Комнаты не найдены/i)).toBeInTheDocument();
    });
  });

  it('карточка ведёт на правильный URL комнаты', async () => {
    render(<CasinoLobbyPage />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText('Crash VIP')).toBeInTheDocument();
    });

    const roomLink = screen.getByRole('link', { name: /Crash VIP/i });
    expect(roomLink).toHaveAttribute('href', '/casino/rooms/room-1');
  });
});