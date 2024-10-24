import aiohttp
from bs4 import BeautifulSoup
from typing import Optional


async def fetch_text(url: str) -> Optional[str]:
    """Asynchronously fetches the content of a webpage."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                html: str = await response.text()
                return html
    except Exception as e:
        raise ValueError(f"Error fetching content from {url}: {str(e)}")


async def scrape_text(url: str) -> str:
    """Asynchronously scrapes the text content from a webpage."""
    html: str = await fetch_text(url)
    soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
    text: str = soup.get_text(separator=" ", strip=True)
    return text
