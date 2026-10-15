"""Hermes Conductor plugin registration.

This intentionally uses documented plugin registration only.  Lane adapters and
policy gates will be added behind integration tests against released Hermes.
"""
from __future__ import annotations


def _status(raw_args: str) -> str:
    """Return a safe status message while the compatibility POC is developed."""
    if raw_args.strip() not in {"", "help"}:
        return "Usage: /conductor-status"
    return "Hermes Conductor is installed; policy lanes are not configured yet."


def register(ctx) -> None:
    """Register only supported public plugin surfaces."""
    if not ctx.get_config("enabled", default=True):
        return
    ctx.register_command(
        "conductor-status",
        handler=_status,
        description="Show Hermes Conductor policy status",
    )
