"""Main.py: Home of the GrabLib class."""

import asyncio
import hashlib

import requests


class GrabLib:
    """Image Grabber: Downloads files from HTTP servers."""

    def __init__(self):
        """Initialize GrabLib."""

    def __enter__(self):
        """Elevate the Self."""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Eliminate the Self."""

    async def get(self, file_url):
        """Retrieve the provided URL."""
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, requests.get, file_url
            )
            data = response.content
            if response.status_code != 200:
                file_sha256 = "0" * 64
                data = f"Error: {response.status_code}".encode()
            else:
                sha256 = hashlib.sha256()
                sha256.update(response.content)
                file_sha256 = sha256.hexdigest()
        except Exception as ex:
            file_sha256 = "0" * 64
            data = f"Exception: {type(ex).__name__}".encode()
        return {"url": file_url, "sha256": file_sha256, "data": data}
