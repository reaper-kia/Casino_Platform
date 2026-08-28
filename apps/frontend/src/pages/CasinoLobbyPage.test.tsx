import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi, beforeEach, afterEach } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import type { ReactNode } from 'react';
import { CasinoLobbyPage } from './CasinoLobbyPage';

const wrapper = ({ children }: { children: ReactNode }) => {
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

function makeGatewayErrorResponse() {
  return {
    ok: false,
    status: 400,
    headers: { get: () => null },
    json: async () => ({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Request validation failed',
        request_id: 'req-123',
        details: [],
      },
    }),
    text: async () => '',
  } as unknown as Response;
}

describe('CasinoLobbyPage', () => {
  beforeEach(() => {
    vi.stubEnv('VITE_API_MODE', 'mock');
  });

  afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
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

    // crash + archived: такого пересечения в mock нет -> пусто
    const gameTypeSelect = screen.getByLabelText(/Тип игры/i);
    await user.selectOptions(gameTypeSelect, 'crash');

    const statusSelect = screen.getByLabelText(/Статус/i);
    await user.selectOptions(statusSelect, 'archived');

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

  it('пагинация подгружает следующую страницу', async () => {
    const user = userEvent.setup();
    render(<CasinoLobbyPage />, { wrapper });

    // Первая страница: 4 комнаты (DEFAULT_PAGE_SIZE = 4)
    await waitFor(() => {
      expect(screen.getAllByRole('link')).toHaveLength(4);
    });

    const moreButton = screen.getByRole('button', { name: /Загрузить ещё/i });
    await user.click(moreButton);

    // После догрузки: все 6 комнат, кнопка исчезает
    await waitFor(() => {
      expect(screen.getAllByRole('link')).toHaveLength(6);
    });
    expect(
      screen.queryByRole('button', { name: /Загрузить ещё/i }),
    ).not.toBeInTheDocument();
  });

  it('ошибка Gateway показывает ErrorState и кнопку retry', async () => {
    vi.stubEnv('VITE_API_MODE', 'real');
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(makeGatewayErrorResponse()));

    render(<CasinoLobbyPage />, { wrapper });

    expect(
      await screen.findByText(/Request validation failed/i),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('button', { name: /Попробовать снова/i }),
    ).toBeInTheDocument();
  });
});