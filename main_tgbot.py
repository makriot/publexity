import os
import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from src.parsers import ArticlesRetriever, GoogleScholarFetcher
from src.bot_formats import format_articles
from src.database import DatabaseSQLite


# Teleram bot setup
logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher()

articles_retriever = ArticlesRetriever([GoogleScholarFetcher])
database = DatabaseSQLite('articles.db')


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Hi!\nI'm Publexity bot!\nI find articles and "
                         "retrieve key information and links to sources"
                         " by your text query.")


@dp.message(Command("help"))
async def send_help(message: types.Message):
    await message.answer("/start — welcome message\n/help — this message\n"
                         "Send any text query to get article!")


@dp.message()
async def retrieve_articles(message: types.Message):
    articles = await articles_retriever.fetch_sources(message.text)

    await database.insert(message.from_user.id, message.text, articles)

    content = format_articles(articles)
    await message.reply(**content.as_kwargs())


async def main():
    await database.open_connection()
    await articles_retriever.create_session()
    await dp.start_polling(bot)
    await articles_retriever.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        asyncio.run(database.close_connection())
