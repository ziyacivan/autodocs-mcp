"""Generic HTML crawler as fallback for unknown formats."""

import httpx
from typing import List, Dict, Set
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


async def scrape_generic(
    base_url: str,
    client: httpx.AsyncClient,
    max_depth: int = 5,
    max_pages: int = 500,
) -> List[Dict[str, str]]:
    """
    Generic HTML crawler for documentation sites.
    
    Args:
        base_url: Base URL to start crawling from
        client: HTTP client for making requests
        max_depth: Maximum depth to crawl
        max_pages: Maximum number of pages to crawl
        
    Returns:
        List of page metadata dictionaries
    """
    # Normalize base URL
    if not base_url.endswith("/"):
        base_url = base_url + "/"
    
    base_domain = urlparse(base_url).netloc
    visited: Set[str] = set()
    pages: Dict[str, Dict[str, str]] = {}
    queue: List[tuple[str, int]] = [(base_url, 0)]  # (url, depth)
    
    while queue and len(pages) < max_pages:
        url, depth = queue.pop(0)
        
        if depth > max_depth:
            continue
        
        normalized_url = normalize_url(url)
        if normalized_url in visited:
            continue
        
        visited.add(normalized_url)
        
        try:
            response = await client.get(normalized_url, timeout=10.0, follow_redirects=True)
            if response.status_code != 200:
                continue
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Extract title
            title = None
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text(strip=True)
            if not title:
                h1_tag = soup.find("h1")
                if h1_tag:
                    title = h1_tag.get_text(strip=True)
            if not title:
                title = extract_title_from_url(normalized_url)
            
            # Store page
            pages[normalized_url] = {
                "url": normalized_url,
                "title": title,
                "type": "page",
                "format": "generic",
            }
            
            # Find links for next depth
            if depth < max_depth:
                for link in soup.find_all("a", href=True):
                    href = link.get("href")
                    if not href:
                        continue
                    
                    # Resolve relative URLs
                    full_url = urljoin(normalized_url, href)
                    parsed = urlparse(full_url)
                    
                    # Only follow same-domain links
                    if parsed.netloc == base_domain:
                        # Remove fragments
                        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                        if clean_url not in visited:
                            queue.append((clean_url, depth + 1))
        
        except Exception:
            # Skip pages that fail to load
            continue
    
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
        parts = path.split("/")
        title = parts[-1].replace("-", " ").replace("_", " ").title()
        return title
    return "Home"



