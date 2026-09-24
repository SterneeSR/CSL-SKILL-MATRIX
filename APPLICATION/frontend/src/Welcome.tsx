import { useNavigate } from 'react-router-dom';
import { api } from './api';

interface WelcomeProps {
  user: {
    email: string;
    name: string;
  } | null;
  onLogout: () => void;
}

export function Welcome({ user, onLogout }: WelcomeProps) {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await api.post('/logout/');
    } catch {
      // ignore
    } finally {
      onLogout();
      navigate('/login');
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: '60px auto', textAlign: 'center' }}>
      <h1>Welcome to CSL</h1>
      {user && (
        <div style={{ margin: '20px 0' }}>
          <p><strong>Name:</strong> {user.name || '(not set)'}</p>
          <p><strong>Email:</strong> {user.email}</p>
        </div>
      )}
      <button onClick={handleLogout} style={{ padding: '8px 16px', marginTop: 16 }}>
        Logout
      </button>
    </div>
  );
}
