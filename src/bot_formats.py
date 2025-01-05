from typing import List

from aiogram.utils.formatting import Text, Bold, TextLink, Italic, as_line

from src.objects import ArticleHandler


def format_article(article: ArticleHandler) -> Text:
    components = []
    if article.name and article.authors:
        components.append(
            as_line(Bold(article.name), Italic(" (", article.authors, ")"))
        )
    elif article.name:
        components.append(
            as_line(Bold(article.name))
        )
    if article.url and article.pdf_url:
        components.append(
            as_line(TextLink("pdf", url=article.pdf_url), " | ", TextLink("source", url=article.url))
        )
    elif article.url:
        components.append(
            as_line(TextLink("source", url=article.url))
        )
    elif article.pdf_url:
        components.append(
            as_line(TextLink("pdf", url=article.pdf_url))
        )
    if article.summarized:
        components.append(
            as_line(Text(article.summarized))
        )
    if article.name:
        components.append(
            as_line(Text("Cited: ", f"{article.cited}"))
        )

    return Text(*components)


def format_articles(articles: List[ArticleHandler | None]) -> Text:
    list_formatted = []
    for article in articles:
        if article is not None:
            list_formatted.append(format_article(article))
    if not list_formatted:
        content = Text("No articles found for your query")
    else:
        content = Text(*list_formatted)
    return content
