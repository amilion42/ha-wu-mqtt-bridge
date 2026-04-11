"""Async forwarding of weather data to the real Weather Underground servers."""

import asyncio
import logging
from urllib.parse import urlencode

import aiohttp

logger = logging.getLogger(__name__)


PI2_IP="192.168.1.181"
PI2_PATH="/actu_log/"


class PI2Forwarder:
    """Forwards weather data to the real PI2 server.
    """

    def __init__(self, enabled: bool = True):
        self._enabled = enabled
        self._session: aiohttp.ClientSession | None = None

    async def start(self) -> None:
        """create HTTP session."""
        if not self._enabled:
            logger.info("PI2 forwarding is disabled")
            return
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10),
        )
        logger.info("PI2 forwarding enabled")

    async def stop(self) -> None:
        """Close the HTTP session and stop background tasks."""
        if self._session:
            await self._session.close()
            self._session = None

    async def forward(self, params: dict[str, str]) -> None:
        """Forward weather data to the real PI2 server (fire-and-forget).

        This should be called as a background task. Failures are logged
        but never raised — they must not affect local MQTT publishing.
        """
        if not self._enabled or not self._session:
            return

        # Forward to the primary host (rtupdate)
        ip = PI2_IP
        if not ip:
            return

        url = f"http://{ip}{PI2_PATH}"
        query = urlencode(params)
        full_url = f"{url}?{query}"
        logger.debug("Forwarded to PI2 (%s): ", full_url)

        try:
            async with self._session.get(
                full_url,
                headers={"Host": ip},
                ssl=False,  # Don't verify WU's cert when connecting by IP
            ) as resp:
                body = await resp.text()
                if "success" in body.lower():
                    logger.debug("Forwarded to PI2 (%s): success", ip)
                else:
                    logger.warning("PI2 forward response (%s): %s", ip, body[:200])
        except Exception:
            logger.warning("Failed to forward to PI2 (%s)", ip, exc_info=True)

