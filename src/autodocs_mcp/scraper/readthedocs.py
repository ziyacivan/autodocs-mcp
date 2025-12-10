"""Main ReadTheDocs scraper with format detection and fallback."""

import httpx
from typing import List, Dict, Optional
from tqdm.asyncio import tqdm

from .detector import detect_format
from .sphinx import scrape_sphinx
from .mkdocs import scrape_mkdocs
from .fallback import scrape_generic
from .parser import fetch_and_parse_page


class ReadTheDocsScraper:
    """Scraper for ReadTheDocs documentation with format detection."""

    def __init__(
        self,
        base_url: str,
        rate_limit: float = 1.0,
        max_retries: int = 3,
    ):
        """
        Initialize the scraper.

        Args:
            base_url: Base URL of the ReadTheDocs documentation
            rate_limit: Seconds to wait between requests
            max_retries: Maximum number of retries for failed requests
        """
        self.base_url = base_url.rstrip("/")
        self.rate_limit = rate_limit
        self.max_retries = max_retries
        self.client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=10, max_connections=20),
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.client:
            await self.client.aclose()

    async def detect_and_scrape(self) -> List[Dict[str, str]]:
        """
        Detect format and scrape documentation pages.

        Returns:
            List of page metadata dictionaries
        """
        if not self.client:
            raise RuntimeError("Scraper must be used as async context manager")

        # Detect format
        format_type = await detect_format(self.base_url, self.client)

        # Scrape based on format
        if format_type == "sphinx":
            pages = await scrape_sphinx(self.base_url, self.client)
        elif format_type == "mkdocs":
            pages = await scrape_mkdocs(self.base_url, self.client)
        else:
            pages = await scrape_generic(self.base_url, self.client)

        return pages

    async def fetch_all_content(
        self,
        pages: List[Dict[str, str]],
        progress: bool = True,
    ) -> List[Dict[str, str]]:
        """
        Fetch content for all pages.

        Args:
            pages: List of page metadata dictionaries
            progress: Whether to show progress bar

        Returns:
            List of pages with content added
        """
        if not self.client:
            raise RuntimeError("Scraper must be used as async context manager")

        results = []

        if progress:
            iterator = tqdm(pages, desc="Fetching pages")
        else:
            iterator = pages

        for page_meta in iterator:
            try:
                content_data = await fetch_and_parse_page(page_meta["url"], self.client)

                # Merge metadata with content
                result = {
                    **page_meta,
                    **content_data,
                }
                results.append(result)
            except Exception as e:
                # Log error but continue
                print(f"Warning: Failed to fetch {page_meta['url']}: {e}")
                continue

        return results
