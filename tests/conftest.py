"""Shared pytest configuration.

The API module initializes Sentry at import time. Without intervention, any
error captured while running the test suite (including errors that tests
trigger on purpose, such as the "credentials not configured" 500 path) would be
sent to the real Sentry project and tagged as ``production``.

This conftest keeps the Sentry client fully initialized (so instrumentation
behaves exactly as in production) but routes all envelopes to an in-memory
transport instead of the network, and tags test runs with the ``test``
environment.
"""

import os
from collections.abc import Iterator
from typing import Any

# Must run before any test module imports ``src.pipeline.api``.
os.environ.setdefault("SENTRY_ENVIRONMENT", "test")

import pytest
import sentry_sdk
from sentry_sdk.envelope import Envelope
from sentry_sdk.transport import Transport


class InMemoryTransport(Transport):
    """Sentry transport that records envelopes instead of sending them."""

    def __init__(self, options: dict[str, Any] | None = None) -> None:
        super().__init__(options)
        self.envelopes: list[Envelope] = []

    def capture_envelope(self, envelope: Envelope) -> None:
        self.envelopes.append(envelope)

    def flush(self, timeout: float, callback: Any | None = None) -> None:
        return None

    def kill(self) -> None:
        return None

    def events(self) -> list[dict[str, Any]]:
        """Return captured error events (excluding transactions, logs, etc.)."""
        events: list[dict[str, Any]] = []
        for envelope in self.envelopes:
            for item in envelope.items:
                if item.type == "event" and item.payload.json is not None:
                    events.append(item.payload.json)
        return events


@pytest.fixture(scope="session", autouse=True)
def sentry_transport() -> Iterator[InMemoryTransport]:
    """Replace the Sentry client's network transport for the whole session."""
    # Ensure the API module (and therefore sentry_sdk.init) has been imported.
    import src.pipeline.api  # noqa: F401

    client = sentry_sdk.get_client()
    original_transport = client.transport
    if original_transport is not None:
        original_transport.kill()
    transport = InMemoryTransport(client.options)
    client.transport = transport
    # Do not restore the original transport: the SDK flushes pending
    # envelopes at interpreter exit and they must not reach the network.
    yield transport


@pytest.fixture
def sentry_events(sentry_transport: InMemoryTransport) -> InMemoryTransport:
    """Expose captured Sentry envelopes, cleared at the start of each test."""
    sentry_transport.envelopes.clear()
    return sentry_transport
