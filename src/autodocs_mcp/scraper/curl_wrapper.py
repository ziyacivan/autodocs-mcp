"""Wrapper to make curl_cffi compatible with httpx-like interface."""

from typing import Optional
from curl_cffi.requests import AsyncSession, Response as CurlResponse


class CurlCffiResponse:
    """Wrapper to make curl_cffi Response look like httpx Response."""

    def __init__(self, response: CurlResponse):
        self._response = response

    @property
    def status_code(self) -> int:
        return self._response.status_code

    @property
    def headers(self):
        return self._response.headers

    @property
    def content(self) -> bytes:
        return self._response.content

    @property
    def text(self) -> str:
        return self._response.text

    async def aclose(self):
        """Close response (no-op for curl_cffi)."""
        pass

    def raise_for_status(self):
        """Raise exception for bad status codes."""
        if 400 <= self.status_code < 600:
            raise Exception(f"HTTP {self.status_code}: {self.text[:100]}")


class CurlCffiWrapper:
    """Wrapper to make curl_cffi AsyncSession look like httpx.AsyncClient."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(
        self,
        url: str,
        timeout: Optional[float] = None,
        follow_redirects: bool = True,
        **kwargs,
    ) -> CurlCffiResponse:
        """Make GET request."""
        response = await self._session.get(
            url,
            timeout=timeout,
            allow_redirects=follow_redirects,
            **kwargs,
        )
        return CurlCffiResponse(response)

    async def head(
        self,
        url: str,
        timeout: Optional[float] = None,
        follow_redirects: bool = True,
        **kwargs,
    ) -> CurlCffiResponse:
        """Make HEAD request."""
        response = await self._session.head(
            url,
            timeout=timeout,
            allow_redirects=follow_redirects,
            **kwargs,
        )
        return CurlCffiResponse(response)

    async def aclose(self):
        """Close the session."""
        await self._session.close()
