"""Sphinx documentation scraper using objects.inv."""

import httpx
from typing import List, Dict
from urllib.parse import urljoin, urlparse
from sphobjinv import Inventory


async def scrape_sphinx(base_url: str, client: httpx.AsyncClient) -> List[Dict[str, str]]:
    """
    Scrape Sphinx documentation using objects.inv file.

    Args:
        base_url: Base URL of the documentation
        client: HTTP client for making requests

    Returns:
        List of page metadata dictionaries with 'url', 'title', 'type', etc.
    """
    # Normalize base URL
    if not base_url.endswith("/"):
        base_url = base_url + "/"

    # Download objects.inv
    objects_inv_url = urljoin(base_url, "objects.inv")
    try:
        response = await client.get(objects_inv_url, timeout=10.0)
        response.raise_for_status()
    except Exception as e:
        raise ValueError(f"Failed to download objects.inv: {e}")

    # Parse inventory
    # sphobjinv can handle raw bytes directly and will decompress if needed
    inv = Inventory(response.content)

    # Extract unique URLs
    # inv.objects is a list of DataObjStr instances
    pages: Dict[str, Dict[str, str]] = {}

    for obj in inv.objects:
        uri = obj.uri
        if not uri:
            continue

        # Build full URL
        if uri.startswith("/"):
            full_url = urljoin(base_url, uri.lstrip("/"))
        else:
            full_url = urljoin(base_url, uri)

        # Normalize URL
        parsed = urlparse(full_url)
        normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if normalized_url.endswith("/"):
            normalized_url = normalized_url.rstrip("/")

        # Store page metadata
        if normalized_url not in pages:
            pages[normalized_url] = {
                "url": normalized_url,
                "title": obj.dispname or obj.name,
                "type": obj.domain,
                "name": obj.name,
                "format": "sphinx",
            }

    return list(pages.values())
