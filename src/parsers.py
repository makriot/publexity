import re
import sys
import asyncio
import aiohttp
import logging
from abc import ABC, abstractmethod
from typing import List

from yarl import URL
from bs4 import BeautifulSoup

from src.objects import ArticleHandler

# Random address for accessing resources
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

logger = logging.getLogger(__name__)


class FunctionNotCalledError(Exception):
    def __init__(self, message="Required function wasn't called"):
        self.message = message
        super().__init__(self.message)


class Fetcher(ABC):
    URL_BASE: URL

    @classmethod
    @abstractmethod
    def get_url(cls, query: str) -> str:
        pass

    @classmethod
    @abstractmethod
    async def fetch_url(cls, session: aiohttp.ClientSession, query: str) -> ArticleHandler:
        pass


class GoogleScholarFetcher(Fetcher):
    URL_BASE: URL = URL("https://scholar.google.com")

    @classmethod
    def get_url(cls, query: str) -> str:
        """Build url for Google Scholar with query"""
        return str(cls.URL_BASE / "scholar" % {"q": query})

    @staticmethod
    def extract_first_article(soup: BeautifulSoup) -> ArticleHandler | None:
        first_article = soup.find(attrs={"data-rp": "0"})
        pdf_ref = first_article.a.get("href")
        summarized = first_article.find(attrs={"class": "gs_rs"}).get_text()
        naming = first_article.find(attrs={"class": "gs_ri"}).find("a")
        source_ref = naming.get("href")
        naming_text = naming.get_text()

        authors = first_article.find(attrs={"class": "gs_a"}).get_text()

        result = re.search("-", authors)
        if result:
            sep_idx = result.span()[0] - 1
            extracted_authors = authors[:sep_idx]
        else:
            logger.warning(f"Bad authors string: {authors}")
            extracted_authors = authors

        try:
            cited = first_article.find(attrs={"class": "gs_fl gs_flb"}).find_all("a")[2].get_text()
        except AttributeError:
            cited = cited = first_article.find(attrs={"class": "gs_fl gs_flb gs_invis"}).find_all("a")[2].get_text()
        result = re.search(r"\d+", cited)
        if result:
            extracted_cited = result.group()
        else:
            extracted_cited = "0"
        try:
            extracted_cited = int(extracted_cited)
        except ValueError as e:
            logger.warning(f"ValueError in extracting cited -- invalid integer value: {e}")
            extracted_cited = 0

        if None in [source_ref, pdf_ref, naming_text,
                    extracted_authors, summarized, extracted_cited]:
            return None

        return ArticleHandler(
            url=source_ref,
            pdf_url=pdf_ref,
            name=naming_text,
            authors=extracted_authors,
            summarized=summarized,
            cited=extracted_cited
        )


    @classmethod
    async def get_first_article(cls, session: aiohttp.ClientSession, query: str) -> ArticleHandler | None:
        url = cls.get_url(query)
        async with session.get(url, headers=HEADERS) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            try:
                article = cls.extract_first_article(soup)
            except AttributeError as err:
                logger.warning(f"AttributeError in parsing Google Scholar page: {err}")
                return None

            return article


class ArticlesRetriever:
    """
    Async retriever of Articles from fetchers list
    """
    def __init__(self, fetchers: List[Fetcher]):
        self.session: aiohttp.ClientSession | None = None
        self.fetchers: List[Fetcher] = fetchers

    async def create_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def fetch_sources(self, query: str) -> List[ArticleHandler]:
        if self.session is None:
            raise FunctionNotCalledError("create_session() method wasn't called")
        tasks = [fetcher.get_first_article(self.session, query)
                 for fetcher in self.fetchers]
        responses = await asyncio.gather(*tasks)
        return responses

    async def close(self):
        """Close the aiohttp ClientSession."""
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def __aenter__(self):
        self.create_session()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
