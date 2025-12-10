"""Format detection for ReadTheDocs documentation."""

import asyncio
import httpx
from typing import Literal, Optional
from urllib.parse import urljoin


async def _make_request_with_retry(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    max_retries: int = 3,
    timeout: float = 10.0,
    **kwargs,
) -> Optional[httpx.Response]:
    """
    Make an HTTP request with 429 rate limit handling.

    Args:
        client: HTTP client for making requests
        method: HTTP method ('get', 'head', etc.)
        url: URL to request
        max_retries: Maximum number of retries for 429 responses
        timeout: Request timeout in seconds
        **kwargs: Additional arguments to pass to the request method

    Returns:
        Response object if successful, None if all retries exhausted
    """
    for attempt in range(max_retries):
        try:
            request_method = getattr(client, method.lower())
            response = await request_method(url, timeout=timeout, **kwargs)

            # Handle 429 rate limiting
            if response.status_code == 429:
                # Check for Retry-After header
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    try:
                        wait_time = int(retry_after)
                    except ValueError:
                        # If Retry-After is not a number, use exponential backoff
                        wait_time = 2**attempt
                else:
                    # Exponential backoff: 2^attempt seconds
                    wait_time = 2**attempt

                # Cap wait time at 60 seconds
                wait_time = min(wait_time, 60)

                # Close the response to avoid resource leaks
                await response.aclose()

                if attempt < max_retries - 1:
                    if retry_after:
                        try:
                            retry_source = f"Retry-After header ({int(retry_after)}s)"
                        except ValueError:
                            retry_source = "exponential backoff"
                    else:
                        retry_source = "exponential backoff"
                    print(
                        f"⚠️  Rate limit hit (429) for {url}. "
                        f"Waiting {wait_time}s before retry {attempt + 2}/{max_retries} ({retry_source})..."
                    )
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    # Last attempt failed with 429, return None
                    print(f"❌ Rate limit (429) exceeded after {max_retries} attempts for {url}")
                    return None

            return response

        except httpx.HTTPStatusError as e:
            # If it's a 429, we'll handle it in the next iteration
            if e.response.status_code == 429:
                retry_after = e.response.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    wait_time = int(retry_after)
                else:
                    wait_time = 2**attempt
                wait_time = min(wait_time, 60)

                if attempt < max_retries - 1:
                    retry_source = (
                        f"Retry-After header ({retry_after}s)"
                        if retry_after and retry_after.isdigit()
                        else "exponential backoff"
                    )
                    print(
                        f"⚠️  Rate limit hit (429) for {url}. "
                        f"Waiting {wait_time}s before retry {attempt + 2}/{max_retries} ({retry_source})..."
                    )
                    # Close the response to avoid resource leaks
                    await e.response.aclose()
                    await asyncio.sleep(wait_time)
                    continue
                # Close the response before returning
                print(f"❌ Rate limit (429) exceeded after {max_retries} attempts for {url}")
                await e.response.aclose()
                return None
            # For other status errors, return None
            return None
        except Exception:
            # For other exceptions, return None
            return None

    return None


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

    # Try HEAD request first (faster)
    response = await _make_request_with_retry(
        client, "head", objects_inv_url, timeout=10.0, follow_redirects=True
    )
    if response and response.status_code == 200:
        return "sphinx"

    # Try GET request (some servers don't support HEAD)
    response = await _make_request_with_retry(
        client, "get", objects_inv_url, timeout=10.0, follow_redirects=True
    )
    if response and response.status_code == 200:
        # Verify it's actually an objects.inv file by checking content
        content_type = response.headers.get("content-type", "").lower()
        if "text/plain" in content_type or response.content[:4] == b"# Sph":
            return "sphinx"

    # 2. Check for sitemap.xml (MkDocs or other)
    sitemap_url = urljoin(base_url, "sitemap.xml")
    response = await _make_request_with_retry(
        client, "get", sitemap_url, timeout=10.0, follow_redirects=True
    )
    if response and response.status_code == 200:
        content = response.text
        # MkDocs sitemaps typically contain specific patterns
        if "mkdocs" in content.lower() or "urlset" in content.lower():
            return "mkdocs"

    # 3. Check HTML for format indicators
    response = await _make_request_with_retry(
        client, "get", base_url, timeout=10.0, follow_redirects=True
    )
    if response and response.status_code == 200:
        content = response.text.lower()
        # Check for Sphinx indicators
        if "sphinx" in content or "sphinxdoc" in content or "sphinx_rtd_theme" in content:
            return "sphinx"
        # Check for MkDocs indicators
        if "mkdocs" in content or "material" in content:
            return "mkdocs"

    # 4. Fallback to generic
    return "generic"
