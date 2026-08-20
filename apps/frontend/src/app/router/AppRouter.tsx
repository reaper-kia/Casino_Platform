import { Route, Routes } from 'react-router-dom';
import { AppShell } from '../AppShell';
import { HomePage } from '../../pages/HomePage';
import { LoginPage } from '../../pages/LoginPage';
import { RegisterPage } from '../../pages/RegisterPage';
import { CasinoLobbyPage } from '../../pages/CasinoLobbyPage';
import { RoomPage } from '../../pages/RoomPage';
import { NotFoundPage } from '../../pages/NotFoundPage';

export function AppRouter() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/casino" element={<CasinoLobbyPage />} />
        <Route path="/casino/rooms/:roomId" element={<RoomPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}