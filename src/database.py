import sys
import logging
import aiosqlite
from typing import List

from src.objects import ArticleHandler

logger = logging.getLogger(__name__)


class DatabaseSQLite:
    def __init__(self, dbname: str = 'articles.db'):
        self.dbname = dbname
        self.conn = None

    async def open_connection(self):
        """Open the database connection and create the table if it doesn't exist."""
        self.conn = await aiosqlite.connect(self.dbname)
        await self.conn.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            query TEXT,
            url TEXT,
            pdf_url TEXT,
            name TEXT,
            authors TEXT,
            summarized TEXT,
            cited INTEGER
        )
        ''')
        await self.conn.commit()

    async def close_connection(self):
        """Close the database connection."""
        if self.conn:
            await self.conn.close()

    async def insert(self, user_id: int, query: str, articles: List[ArticleHandler]):
        """Insert articles into the database with transaction management."""
        
        # Prepare the SQL statement for inserting a single article
        sql = '''
        INSERT INTO articles (user_id, query, url, pdf_url, name, authors, summarized, cited) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        try:
            await self.conn.execute('BEGIN')
            for article in articles:
                if article:
                    await self.conn.execute(sql, (
                        user_id,
                        query,
                        article.url,
                        article.pdf_url,
                        article.name,
                        article.authors,
                        article.summarized,
                        article.cited
                    ))
            await self.conn.commit()
        except Exception as e:
            await self.conn.rollback()
            logger.warning(f"Error inserting data: {e}")
