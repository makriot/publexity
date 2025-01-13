from fastapi import FastAPI
from fastapi import status
from pydantic import BaseModel
from typing import List

from src.parsers import ArticlesRetriever, GoogleScholarFetcher
from src.objects import ArticleHandler

app = FastAPI(debug=True)


class Post(BaseModel):
    text: str


@app.post("/articles", status_code=status.HTTP_201_CREATED)
async def get_articles(post: Post,
                       response_model=dict[str, List[ArticleHandler]]):
    print(post.text)
    async with ArticlesRetriever([GoogleScholarFetcher]) as articles_retriever:
        articles = await articles_retriever.fetch_sources(post.text)
    return {"articles": articles}
