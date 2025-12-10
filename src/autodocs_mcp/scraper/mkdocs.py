"""MkDocs documentation scraper using sitemap.xml."""

import httpx
from typing import List, Dict
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup


async def scrape_mkdocs(base_url: str, client: httpx.AsyncClient) -> List[Dict[str, str]]:
    """
    Scrape MkDocs documentation using sitemap.xml or HTML navigation.

    Args:
        base_url: Base URL of the documentation
        client: HTTP client for making requests

    Returns:
        List of page metadata dictionaries
    """
    # Normalize base URL
    if not base_url.endswith("/"):
        base_url = base_url + "/"

    pages: Dict[str, Dict[str, str]] = {}

    # Try sitemap.xml first
    sitemap_url = urljoin(base_url, "sitemap.xml")
    try:
        response = await client.get(sitemap_url, timeout=30.0, follow_redirects=True)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
                # Handle sitemap XML format
                namespace = {"sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9"}

                # Find all URL elements
                for url_elem in root.findall(".//sitemap:url", namespace):
                    loc_elem = url_elem.find("sitemap:loc", namespace)
                    if loc_elem is not None:
                        url = loc_elem.text
                        if url:
                            normalized_url = normalize_url(url)
                            if normalized_url not in pages:
                                pages[normalized_url] = {
                                    "url": normalized_url,
                                    "title": extract_title_from_url(url),
                                    "type": "page",
                                    "format": "mkdocs",
                                }
            except ET.ParseError:
                # If XML parsing fails, try HTML navigation
                pass
    except Exception:
        pass

    # Fallback to HTML navigation if sitemap didn't work
    if not pages:
        try:
            response = await client.get(base_url, timeout=30.0, follow_redirects=True)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")

                # Find navigation links
                nav_links = soup.find_all("a", href=True)
                for link in nav_links:
                    href = link.get("href")
                    if href:
                        full_url = urljoin(base_url, href)
                        normalized_url = normalize_url(full_url)

                        # Only include links from same domain
                        if urlparse(normalized_url).netloc == urlparse(base_url).netloc:
                            if normalized_url not in pages:
                                pages[normalized_url] = {
                                    "url": normalized_url,
                                    "title": link.get_text(strip=True)
                                    or extract_title_from_url(normalized_url),
                                    "type": "page",
                                    "format": "mkdocs",
                                }
        except Exception:
            pass

    return list(pages.values())


def normalize_url(url: str) -> str:
    """Normalize URL by removing trailing slashes and fragments."""
    parsed = urlparse(url)
    normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    if normalized.endswith("/") and len(normalized) > 1:
        normalized = normalized.rstrip("/")
    return normalized


def extract_title_from_url(url: str) -> str:
    """Extract a title from URL path."""
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if path:
        # Use last part of path as title
        parts = path.split("/")
        title = parts[-1].replace("-", " ").replace("_", " ").title()
        return title
    return "Home"
