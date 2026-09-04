"""Sample application used as a later scan target. It is not pre-analyzed."""

from datetime import datetime, timezone


def health() -> dict[str, str]:
    return {
        "service": "demo-target",
        "status": "ok",
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    print(health())
