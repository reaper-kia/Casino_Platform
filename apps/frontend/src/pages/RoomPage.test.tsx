import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi, beforeEach, afterEach } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import type { ReactNode } from 'react';
import { RoomPage } from './RoomPage';

const makeWrapper = (initialEntries: string[]) =>
  function Wrapper({ children }: { children: ReactNode }) {
    const queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          // НЕ отключаем retry — даём хуку самому управлять ими
          // Минимальная задержка, чтобы тесты были быстрыми
          retryDelay: 0,
        },
      },
    });
    return (
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={initialEntries}>
          <Routes>
            <Route path="/casino/rooms/:roomId" element={children} />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>
    );
  };

describe('RoomPage', () => {
  beforeEach(() => {
    vi.stubEnv('VITE_API_MODE', 'mock');
  });

  afterEach(() => {
    vi.unstubAllEnvs();
    vi.restoreAllMocks();
  });

  it('рендерит snapshot комнаты и список участников', async () => {
    render(<RoomPage />, { wrapper: makeWrapper(['/casino/rooms/room-1']) });

    expect(await screen.findByText('Crash VIP')).toBeInTheDocument();
    expect(screen.getByText('crash')).toBeInTheDocument();
    expect(screen.getByText('open')).toBeInTheDocument();
    expect(screen.getByText(/3\s*\/\s*100/)).toBeInTheDocument();
    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('Bob')).toBeInTheDocument();
    expect(screen.getByText('Charlie')).toBeInTheDocument();
  });

  it('показывает Private badge для приватной комнаты', async () => {
    render(<RoomPage />, { wrapper: makeWrapper(['/casino/rooms/room-4']) });

    expect(await screen.findByText('Private Crash')).toBeInTheDocument();
    expect(screen.getByText('Private')).toBeInTheDocument();
  });

  it('показывает EmptyState, когда участников нет (closed room)', async () => {
    render(<RoomPage />, { wrapper: makeWrapper(['/casino/rooms/room-3']) });

    expect(await screen.findByText('Dice Duel Pro')).toBeInTheDocument();
    expect(screen.getByText(/Участников нет/i)).toBeInTheDocument();
  });

  it('показывает NotFound для неизвестного roomId', async () => {
    render(<RoomPage />, { wrapper: makeWrapper(['/casino/rooms/unknown-room']) });

    expect(await screen.findByText(/404/)).toBeInTheDocument();
    expect(screen.getByText(/Комната не найдена/i)).toBeInTheDocument();
    expect(
      screen.getByRole('button', { name: /Вернуться в лобби/i }),
    ).toBeInTheDocument();
  });

  it('показывает ErrorState с retry при ошибке API', async () => {
    vi.stubEnv('VITE_API_MODE', 'real');
    const user = userEvent.setup();

    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
        headers: { get: () => null },
        json: async () => ({
          error: {
            code: 'INTERNAL',
            message: 'Boom',
            request_id: 'req-1',
            details: [],
          },
        }),
        text: async () => '',
      }),
    );

    render(<RoomPage />, { wrapper: makeWrapper(['/casino/rooms/room-1']) });

    // Даём больше времени: хук делает 3 попытки (1 + 2 retry) с retryDelay: 0
    expect(
      await screen.findByText('Boom', {}, { timeout: 5000 }),
    ).toBeInTheDocument();

    const retryBtn = screen.getByRole('button', { name: /Попробовать снова/i });
    await user.click(retryBtn);

    // После ручного retry fetch вызывается ещё раз (предыдущие попытки + новый)
    expect(vi.mocked(fetch).mock.calls.length).toBeGreaterThan(1);
  });
});