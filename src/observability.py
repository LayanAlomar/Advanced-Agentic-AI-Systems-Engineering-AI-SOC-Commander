from __future__ import annotations
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, TypeVar

from .config import settings

T = TypeVar("T")

def log_event(run_id: str, node: str, event_type: str, **details: Any) -> None:
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id,
        "node": node,
        "event_type": event_type,
        **details,
    }
    Path(settings.log_path).parent.mkdir(parents=True, exist_ok=True)
    with open(settings.log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def timed(run_id: str, node: str, fn: Callable[..., T], *args: Any, **kwargs: Any) -> tuple[T, float]:
    started = time.perf_counter()
    try:
        result = fn(*args, **kwargs)
        latency_ms = round((time.perf_counter() - started) * 1000, 2)
        log_event(run_id, node, "completed", latency_ms=latency_ms)
        return result, latency_ms
    except Exception as exc:
        latency_ms = round((time.perf_counter() - started) * 1000, 2)
        log_event(run_id, node, "failed", latency_ms=latency_ms, error=str(exc))
        raise
