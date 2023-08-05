"""PDF report rendering utilities."""
import json
import logging
from abc import ABC, abstractmethod

import requests

log = logging.getLogger(__name__)


class PDFRenderer(ABC):
    """Abstract PDF renderer."""

    @abstractmethod
    def render(self, url: str) -> bytes:
        """Render a PDF document content from given URL."""
        pass

    @staticmethod
    def create_renderer_from_config(config):
        """PDF renderer instance factory."""
        if config.BROWSERLESS_API_URL and config.BROWSERLESS_API_TOKEN:
            log.info("Creating Browserless.io PDF renderer")
            return BrowserlessPDFRenderer(
                config.BROWSERLESS_API_URL, config.BROWSERLESS_API_TOKEN
            )

        log.info("No PDF renderer available")
        return None


class BrowserlessPDFRenderer(PDFRenderer):
    """Browserless IO implementation."""

    def __init__(self, api_url: str, api_token: str):
        log.info("BrowserlessPDFRenderer: creating instance with api_url = %r", api_url)
        self.api_url = api_url
        self.api_token = api_token

    def render(self, url: str) -> bytes:
        headers = {
            "Cache-Control": "no-cache",
            "Content-Type": "application/json",
        }
        params = {"token": self.api_token}
        data = {
            "url": url,
            "options": {
                "displayHeaderFooter": True,
                "printBackground": False,
                "format": "A4",
            },
            "gotoOptions": {
                "waitUntil": "networkidle0",
            },
        }
        log.info(
            "BrowserlessPDFRenderer.render: about to send a POST request to "
            "browserless with data = %r and headers = %r",
            json.dumps(data),
            json.dumps(headers),
        )

        # Request server
        r = requests.post(
            self.api_url, headers=headers, params=params, data=json.dumps(data)
        )
        r.raise_for_status()
        log.info(
            "BrowserlessPDFRenderer.render: received response, content size = %d",
            len(r.content),
        )
        return r.content
