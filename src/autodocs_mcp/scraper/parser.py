"""HTML content parser for extracting documentation text."""

import httpx
from typing import Dict
from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse


async def fetch_and_parse_page(url: str, client: httpx.AsyncClient) -> Dict[str, str]:
    """
    Fetch a page and extract its content.

    Args:
        url: URL of the page to fetch
        client: HTTP client for making requests

    Returns:
        Dictionary with 'url', 'title', 'content', 'metadata'
    """
    try:
        response = await client.get(url, timeout=10.0, follow_redirects=True)
        response.raise_for_status()
    except Exception as e:
        raise ValueError(f"Failed to fetch {url}: {e}")

    soup = BeautifulSoup(response.content, "html.parser")

    # Remove script and style elements
    for element in soup(["script", "style", "nav", "footer", "header"]):
        element.decompose()

    # Extract title
    title = None
    title_tag = soup.find("title")
    if title_tag:
        title = title_tag.get_text(strip=True)
    if not title:
        h1_tag = soup.find("h1")
        if h1_tag:
            title = h1_tag.get_text(strip=True)

    # Find main content area
    main_content = None

    # Try common content selectors
    content_selectors = [
        "main",
        "article",
        "[role='main']",
        ".content",
        "#content",
        ".documentation",
        "#documentation",
    ]

    for selector in content_selectors:
        main_content = soup.select_one(selector)
        if main_content:
            break

    # If no main content found, use body
    if not main_content:
        main_content = soup.find("body")

    if main_content:
        # Extract text while preserving code blocks
        content_parts = []

        for element in main_content.descendants:
            if isinstance(element, Tag):
                # Preserve code blocks
                if element.name in ["pre", "code"]:
                    code_text = element.get_text()
                    if code_text.strip():
                        content_parts.append(f"\n```\n{code_text}\n```\n")
                # Extract headings
                elif element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                    heading_text = element.get_text(strip=True)
                    if heading_text:
                        level = int(element.name[1])
                        prefix = "#" * level + " "
                        content_parts.append(f"\n{prefix}{heading_text}\n")

        # Also get all text content
        text_content = main_content.get_text(separator="\n", strip=True)
        if text_content:
            content_parts.append(text_content)

        content = "\n".join(content_parts)
    else:
        content = soup.get_text(separator="\n", strip=True)

    # Clean up content
    content = clean_text(content)

    return {
        "url": url,
        "title": title or extract_title_from_url(url),
        "content": content,
        "format": "html",
    }


def clean_text(text: str) -> str:
    """Clean extracted text."""
    # Remove excessive whitespace
    lines = text.split("\n")
    cleaned_lines = []
    prev_empty = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if not prev_empty:
                cleaned_lines.append("")
                prev_empty = True
        else:
            cleaned_lines.append(stripped)
            prev_empty = False

    return "\n".join(cleaned_lines).strip()


def extract_title_from_url(url: str) -> str:
    """Extract a title from URL path."""
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if path:
        parts = path.split("/")
        title = parts[-1].replace("-", " ").replace("_", " ").title()
        return title
    return "Home"
