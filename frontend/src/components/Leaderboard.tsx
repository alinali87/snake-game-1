import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './Leaderboard.css';

interface LeaderboardEntry {
  id: number;
  username: string;
  score: number;
  snake_length: number;
  game_mode: string;
  rank: number | null;
  created_at: string;
}

interface UserStats {
  username?: string;
  games_played: number;
  total_score: number;
  best_score: number;
  average_score: number;
}

type GameMode = 'all' | 'walls' | 'pass-through';

export function Leaderboard() {
  const { user } = useAuth();
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [userStats, setUserStats] = useState<UserStats | null>(null);
  const [selectedMode, setSelectedMode] = useState<GameMode>('all');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchLeaderboard();
  }, [selectedMode]);

  useEffect(() => {
    if (user) {
      fetchUserStats();
    }
  }, [user]);

  const fetchLeaderboard = async () => {
    setIsLoading(true);
    try {
      const url = selectedMode === 'all'
        ? '/api/leaderboard?limit=20'
        : `/api/leaderboard?game_mode=${selectedMode}&limit=20`;

      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        setEntries(data);
      }
    } catch (error) {
      console.error('Failed to fetch leaderboard:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchUserStats = async () => {
    if (!user?.username) return;

    try {
      const response = await fetch(`/api/leaderboard/stats/${user.username}`);
      if (response.ok) {
        const data = await response.json();
        if (!data.error) {
          setUserStats(data);
        }
      }
    } catch (error) {
      console.error('Failed to fetch user stats:', error);
    }
  };

  const getMedalEmoji = (rank: number) => {
    switch (rank) {
      case 1: return '🥇';
      case 2: return '🥈';
      case 3: return '🥉';
      default: return '';
    }
  };

  const getModeIcon = (mode: string) => {
    return mode === 'walls' ? '🧱' : '🌀';
  };

  const getModeName = (mode: string) => {
    return mode === 'walls' ? 'Walls' : 'Pass-Through';
  };

  return (
    <div className="leaderboard-container">
      <h2>🏆 Leaderboard</h2>

      {user && userStats && (
        <div className="user-stats">
          <h3>Your Stats</h3>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-label">Games Played</div>
              <div className="stat-value">{userStats.games_played}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Best Score</div>
              <div className="stat-value">{userStats.best_score}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Average Score</div>
              <div className="stat-value">{userStats.average_score}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Total Score</div>
              <div className="stat-value">{userStats.total_score}</div>
            </div>
          </div>
        </div>
      )}

      <div className="mode-filter">
        <button
          className={selectedMode === 'all' ? 'active' : ''}
          onClick={() => setSelectedMode('all')}
        >
          All Modes
        </button>
        <button
          className={selectedMode === 'walls' ? 'active' : ''}
          onClick={() => setSelectedMode('walls')}
        >
          🧱 Walls
        </button>
        <button
          className={selectedMode === 'pass-through' ? 'active' : ''}
          onClick={() => setSelectedMode('pass-through')}
        >
          🌀 Pass-Through
        </button>
      </div>

      {isLoading ? (
        <div className="loading">Loading leaderboard...</div>
      ) : entries.length === 0 ? (
        <div className="empty-state">
          <p>No scores yet. Be the first to play!</p>
        </div>
      ) : (
        <div className="leaderboard-table-container">
          <table className="leaderboard-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Player</th>
                <th>Score</th>
                <th>Length</th>
                <th>Mode</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {entries.map((entry, index) => {
                const displayRank = selectedMode === 'all' ? index + 1 : entry.rank || index + 1;
                const isCurrentUser = user?.username === entry.username;

                return (
                  <tr key={entry.id} className={isCurrentUser ? 'current-user' : ''}>
                    <td className="rank-cell">
                      <span className="rank-number">{displayRank}</span>
                      {displayRank <= 3 && (
                        <span className="medal">{getMedalEmoji(displayRank)}</span>
                      )}
                    </td>
                    <td className="username-cell">
                      {entry.username}
                      {isCurrentUser && <span className="you-badge">You</span>}
                    </td>
                    <td className="score-cell">{entry.score.toLocaleString()}</td>
                    <td className="length-cell">{entry.snake_length}</td>
                    <td className="mode-cell">
                      <span className="mode-badge">
                        {getModeIcon(entry.game_mode)} {getModeName(entry.game_mode)}
                      </span>
                    </td>
                    <td className="date-cell">
                      {new Date(entry.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
