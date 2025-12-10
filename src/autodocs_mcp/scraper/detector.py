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
    # Try HEAD first, then GET if HEAD fails
    objects_inv_url = urljoin(base_url, "objects.inv")
    try:
        # Try HEAD request first (faster)
        try:
            response = await client.head(objects_inv_url, timeout=10.0, follow_redirects=True)
            if response.status_code == 200:
                return "sphinx"
        except Exception:
            # If HEAD fails, try GET
            pass

        # Try GET request (some servers don't support HEAD)
        response = await client.get(objects_inv_url, timeout=10.0, follow_redirects=True)
        if response.status_code == 200:
            # Verify it's actually an objects.inv file by checking content
            content_type = response.headers.get("content-type", "").lower()
            if "text/plain" in content_type or response.content[:4] == b"# Sph":
                return "sphinx"
    except Exception:
        pass

    # 2. Check for sitemap.xml (MkDocs or other)
    sitemap_url = urljoin(base_url, "sitemap.xml")
    try:
        # Try GET directly (more reliable than HEAD)
        response = await client.get(sitemap_url, timeout=10.0, follow_redirects=True)
        if response.status_code == 200:
            content = response.text
            # MkDocs sitemaps typically contain specific patterns
            if "mkdocs" in content.lower() or "urlset" in content.lower():
                return "mkdocs"
    except Exception:
        pass

    # 3. Check HTML for format indicators
    try:
        response = await client.get(base_url, timeout=10.0, follow_redirects=True)
        if response.status_code == 200:
            content = response.text.lower()
            # Check for Sphinx indicators
            if "sphinx" in content or "sphinxdoc" in content or "sphinx_rtd_theme" in content:
                return "sphinx"
            # Check for MkDocs indicators
            if "mkdocs" in content or "material" in content:
                return "mkdocs"
    except Exception:
        pass

    # 4. Fallback to generic
    return "generic"
