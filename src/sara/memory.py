import aiosqlite

class MemoryStore:
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path

    async def initialize(self) -> None:
        async with aiosqlite.connect(self.database_path) as db:
            await db.executescript("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, fact TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                CREATE VIRTUAL TABLE IF NOT EXISTS conversation_fts USING fts5(user_id UNINDEXED, body);
            """)
            await db.commit()

    async def context_for(self, user_id: int, query: str, limit: int = 5) -> list[str]:
        async with aiosqlite.connect(self.database_path) as db:
            cursor = await db.execute("SELECT fact FROM memories WHERE user_id=? ORDER BY id DESC LIMIT ?", (user_id, limit))
            facts = [row[0] for row in await cursor.fetchall()]
            tokens = " OR ".join(word for word in query.split() if len(word) > 3)
            if not tokens:
                return facts
            try:
                cursor = await db.execute("SELECT body FROM conversation_fts WHERE user_id=? AND conversation_fts MATCH ? LIMIT ?", (user_id, tokens, limit))
                facts.extend(row[0] for row in await cursor.fetchall())
            except aiosqlite.OperationalError:
                pass
            return facts

    async def record_turn(self, user_id: int, body: str) -> None:
        async with aiosqlite.connect(self.database_path) as db:
            await db.execute("INSERT INTO conversation_fts(user_id, body) VALUES (?, ?)", (user_id, body))
            await db.commit()