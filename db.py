from logging import getLogger
from pathlib import Path
from sqlite3 import connect


_INIT_DB_SQL: str = """
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE COLLATE NOCASE,
    best_score INTEGER NOT NULL DEFAULT 0,
    games_played INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
)
"""

# updated_at changes only when the best score improves, so on equal scores
# the player who reached that score first ranks higher.
_SAVE_RESULT_SQL: str = """
INSERT INTO players (name, best_score, games_played) VALUES (?, ?, 1)
ON CONFLICT(name) DO UPDATE SET
    best_score = MAX(best_score, excluded.best_score),
    games_played = games_played + 1,
    updated_at = CASE
        WHEN excluded.best_score > best_score THEN datetime('now')
        ELSE updated_at
    END
"""

_GET_TOP_PLAYERS_SQL: str = """
SELECT name AS nickname, best_score FROM players
ORDER BY best_score DESC, updated_at ASC
LIMIT ?
"""


class ScoreRepository:

    def __init__(self, path: Path) -> None:

        self._logger = getLogger(__name__)

        self._logger.debug('Connecting to database at %r', path)

        self._connection = connect(path)

        self._logger.debug('Initializing database schema')

        with self._connection:
            self._connection.execute(_INIT_DB_SQL)

        self._logger.debug('Database schema initialized successfully')

    def save_result(self, name: str, score: int) -> None:
        """
        Insert a new player or update an existing one with a finished game.
        """

        self._logger.debug('Saving result for player %r: %d', name, score)

        with self._connection:
            self._connection.execute(_SAVE_RESULT_SQL, (name, score))

        self._logger.debug('Result successfully saved for player %r', name)

    def get_top_players(self, limit: int) -> list[tuple[str, int]]:
        """
        Return list of ``(nickname, best_score)`` pairs for the best players.
        """

        self._logger.debug('Fetching top %d players', limit)

        cursor = self._connection.execute(_GET_TOP_PLAYERS_SQL, (limit,))

        return [(name, int(score)) for name, score in cursor.fetchall()]

    def close(self) -> None:

        self._logger.debug('Closing database connection')

        self._connection.close()
