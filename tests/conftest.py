"""Pytest configuration for API request context using Playwright."""

from typing import Generator

import pytest
from playwright.sync_api import Playwright, APIRequestContext

from constants import JOKE_API_URL


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:

    request_context = playwright.request.new_context(
        base_url=JOKE_API_URL
    )
    yield request_context
    request_context.dispose()