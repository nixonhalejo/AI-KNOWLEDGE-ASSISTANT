import sqlite3
from contextlib import closing
from pathlib import Path
from uuid import uuid4


class MemoryRepository:
    """Persistencia SQLite; cada operación utiliza su propia conexión."""

    def __init__(self, db_path: str):
        self.db_path = str(db_path)
        Path(self.db_path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(
            self.db_path,
            timeout=5,
        )
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _initialize(self) -> None:
        with closing(self._connect()) as conn:
            with conn:
                conn.executescript("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        id TEXT PRIMARY KEY,
                        created_at TEXT NOT NULL
                            DEFAULT CURRENT_TIMESTAMP
                    );

                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        conversation_id TEXT NOT NULL,
                        role TEXT NOT NULL
                            CHECK (role IN ('user', 'assistant')),
                        content TEXT NOT NULL,
                        FOREIGN KEY (conversation_id)
                            REFERENCES conversations(id)
                            ON DELETE CASCADE
                    );

                    CREATE INDEX IF NOT EXISTS idx_messages_conversation
                        ON messages(conversation_id, id);

                    CREATE TABLE IF NOT EXISTS memories (
                        id TEXT PRIMARY KEY,
                        conversation_id TEXT NOT NULL,
                        fact TEXT NOT NULL,
                        FOREIGN KEY (conversation_id)
                            REFERENCES conversations(id)
                            ON DELETE CASCADE
                    );
                """)

    def create_conversation(self) -> str:
        conversation_id = str(uuid4())

        with closing(self._connect()) as conn:
            with conn:
                conn.execute(
                    "INSERT INTO conversations(id) VALUES (?)",
                    (conversation_id,),
                )

        return conversation_id

    def conversation_exists(
        self,
        conversation_id: str,
    ) -> bool:
        with closing(self._connect()) as conn:
            return conn.execute(
                "SELECT 1 FROM conversations WHERE id = ?",
                (conversation_id,),
            ).fetchone() is not None

    def list_conversations(self) -> list[dict]:
        with closing(self._connect()) as conn:
            rows = conn.execute(
                """
                SELECT id, created_at
                FROM conversations
                ORDER BY created_at DESC, id
                """
            ).fetchall()

        return [
            {
                "conversation_id": row[0],
                "created_at": row[1],
            }
            for row in rows
        ]

    def list_messages(
        self,
        conversation_id: str,
        limit: int = 200,
    ) -> list[dict[str, str]]:
        with closing(self._connect()) as conn:
            rows = conn.execute(
                """
                SELECT role, content
                FROM messages
                WHERE conversation_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (conversation_id, limit),
            ).fetchall()

        return [
            {"role": row[0], "content": row[1]}
            for row in reversed(rows)
        ]

    def save_turn(
        self,
        conversation_id: str,
        question: str,
        answer: str,
    ) -> None:
        # La pregunta y su respuesta se guardan
        # dentro de una única transacción.
        with closing(self._connect()) as conn:
            with conn:
                conn.executemany(
                    """
                    INSERT INTO messages(
                        conversation_id, role, content
                    )
                    VALUES (?, ?, ?)
                    """,
                    [
                        (conversation_id, "user", question),
                        (conversation_id, "assistant", answer),
                    ],
                )

    def list_memories(
        self,
        conversation_id: str,
    ) -> list[dict[str, str]]:
        with closing(self._connect()) as conn:
            rows = conn.execute(
                """
                SELECT id, fact
                FROM memories
                WHERE conversation_id = ?
                ORDER BY rowid
                """,
                (conversation_id,),
            ).fetchall()

        return [
            {"memory_id": row[0], "fact": row[1]}
            for row in rows
        ]

    def add_memory(
        self,
        conversation_id: str,
        fact: str,
    ) -> dict[str, str]:
        memory_id = str(uuid4())

        with closing(self._connect()) as conn:
            with conn:
                conn.execute(
                    """
                    INSERT INTO memories(
                        id, conversation_id, fact
                    )
                    VALUES (?, ?, ?)
                    """,
                    (memory_id, conversation_id, fact),
                )

        return {
            "memory_id": memory_id,
            "fact": fact,
        }

    def delete_memory(
        self,
        conversation_id: str,
        memory_id: str,
    ) -> bool:
        with closing(self._connect()) as conn:
            with conn:
                cursor = conn.execute(
                    """
                    DELETE FROM memories
                    WHERE conversation_id = ?
                      AND id = ?
                    """,
                    (conversation_id, memory_id),
                )

                return cursor.rowcount > 0

    def delete_conversation(
        self,
        conversation_id: str,
    ) -> bool:
        with closing(self._connect()) as conn:
            with conn:
                cursor = conn.execute(
                    """
                    DELETE FROM conversations
                    WHERE id = ?
                    """,
                    (conversation_id,),
                )

                return cursor.rowcount > 0