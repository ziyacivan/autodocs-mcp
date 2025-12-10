"""Format detection for ReadTheDocs documentation."""

import httpx
from typing import Literal
from urllib.parse import urljoin


async def detect_format(
    base_url: str, client: httpx.AsyncClient
) -> Literal["sphinx", "mkdocs", "generic"]:
    """
    Detect the documentation format by checking for format-specific files.

    Args:
        base_url: Base URL of the documentation
        client: HTTP client for making requests

    Returns:
        Detected format: 'sphinx', 'mkdocs', or 'generic'
    """
    # Normalize base URL
    if not base_url.endswith("/"):
        base_url = base_url + "/"

    # 1. Check for objects.inv (Sphinx)
    objects_inv_url = urljoin(base_url, "objects.inv")
    try:
        response = await client.head(objects_inv_url, timeout=5.0)
        if response.status_code == 200:
            return "sphinx"
    except Exception:
        pass

    # 2. Check for sitemap.xml (MkDocs or other)
    sitemap_url = urljoin(base_url, "sitemap.xml")
    try:
        response = await client.head(sitemap_url, timeout=5.0)
        if response.status_code == 200:
            # Try to fetch and check if it's a valid sitemap
            response = await client.get(sitemap_url, timeout=5.0)
            if response.status_code == 200:
                content = response.text
                # MkDocs sitemaps typically contain specific patterns
                if "mkdocs" in content.lower() or "urlset" in content.lower():
                    return "mkdocs"
    except Exception:
        pass

    # 3. Fallback to generic
    return "generic"
