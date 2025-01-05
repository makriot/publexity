from dataclasses import dataclass

@dataclass
class ArticleHandler:
    url: str
    pdf_url: str
    name: str
    authors: str
    summarized: str
    cited: int = 0