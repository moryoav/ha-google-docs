"""Fixtures for Google Docs, using the same HA release as the live instance."""

from collections.abc import Generator
from contextlib import ExitStack
import time
from unittest.mock import MagicMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.google_docs.const import DEFAULT_ACCESS, DOMAIN
from homeassistant.components.application_credentials import (
    ClientCredential,
    async_import_client_credential,
)
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

DOCUMENT_ID = "test-document"
TOKEN_URI = "https://oauth2.googleapis.com/token"


@pytest.fixture(autouse=True)
def custom_integrations(enable_custom_integrations: None) -> None:
    """Allow Home Assistant to load the local custom integration."""


@pytest.fixture
def mock_api() -> Generator[dict[str, MagicMock]]:
    """Mock remote operations without bypassing the HA integration."""
    with ExitStack() as stack:
        mocks = {
            name: stack.enter_context(
                patch(f"custom_components.google_docs.api.{name}")
            )
            for name in ("create_document", "get_document", "append_text")
        }
        mocks["create_document"].return_value = {
            "documentId": DOCUMENT_ID,
            "title": "Home Assistant",
        }
        mocks["get_document"].return_value = {
            "documentId": DOCUMENT_ID,
            "title": "Home Assistant",
            "body": {
                "content": [
                    {"paragraph": {"elements": [{"textRun": {"content": "Hello\n"}}]}}
                ]
            },
        }
        yield mocks


@pytest.fixture
def config_entry() -> MockConfigEntry:
    """Return an authorized configuration entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="Google Docs",
        unique_id=DOCUMENT_ID,
        data={
            "auth_implementation": DOMAIN,
            "token": {
                "access_token": "mock-access-token",
                "refresh_token": "mock-refresh-token",
                "expires_at": time.time() + 3600,
                "scope": DEFAULT_ACCESS,
            },
        },
    )


@pytest.fixture
async def setup_credentials(hass: HomeAssistant) -> None:
    """Register an OAuth application using public HA credential APIs."""
    assert await async_setup_component(hass, "application_credentials", {})
    await async_import_client_credential(
        hass,
        DOMAIN,
        ClientCredential("client-id", "client-secret"),
        DOMAIN,
    )


@pytest.fixture
async def setup_integration(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    mock_api: dict[str, MagicMock],
    setup_credentials: None,
) -> MockConfigEntry:
    """Load a real Google Docs config entry with only Google calls mocked."""
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    return config_entry
