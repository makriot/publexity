# Publexity
**Publexity** is a powerful Telegram bot designed to help users discover and retrieve academic articles, abstracts, and analyses from various online sources. By leveraging multiple databases, Publexity provides a seamless experience for researchers and enthusiasts alike.

## Concept Overview
Publexity should allow users to input queries and receive detailed responses that include:
- **Title**: A well-formatted title of the article.
- **Source**: The originating platform (e.g., Arxiv, Google Scholar).
- **PDF Link**: Direct access to the publication.
- **Abstract**: A summarized version of the abstract for quick understanding.
- **Sources**

The bot should search across several reputable platforms:
- [x] Google Scholar
- [ ] Arxiv
- [ ] Semantic Scholar
- [ ] Reddit
- [ ] Google

## Technology Stack
- aiohttp: For asynchronous HTTP requests.
- yarl: For URL handling.
- BeautifulSoup: For parsing HTML content.

## Features
- [x] shows abstract and meta info
- [x] pdf loading
- [x] User History Tracking: Maintain a SQLite database to save user search history.
- [ ] Dynamic Sources Addition: Continuously integrate new sources for parsing, ensuring up-to-date results.
- [ ] Advanced Summarization: Implement algorithms to extract key sentences from abstracts based on user queries.
- [ ] Article Aggregation: Combine articles scraped from various sources into cohesive summaries.

## User Interaction
- [ ] The bot will feature a command to display the last five searched articles, providing quick access to recent findings. Additionally, users can subscribe to a Telegram channel for updates and news related to the bot's functionalities.

## Future Enhancements
- Establish a database of highly cited AI articles for focused searches.
- Collaborate with experts or platforms like Yandex for technical support and consultation.
- Explore options for integrating a retrieval-augmented generation (RAG) model for enhanced data retrieval capabilities.

This project represents an innovative approach to academic research, creating a personalized experience that not only facilitates article discovery but also visualizes user's interests through tag clouds or thematic classifications.

## Launch bot
With Telegram:

```bash
export BOT_TOKEN=<token>
```
```bash
python main_tgbot.py
```

With FastAPI:

```bash
fastapi dev main_fastapi.py
```

---
We welcome new contributors to the project!
