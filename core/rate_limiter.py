"""
Rate Limiting and Throttling Subsystem for J.A.R.V.I.S.
Provides:
1. In-memory sliding-window IP rate limiting for Flask endpoints.
2. Outgoing API request throttling and exponential backoff retry decorator.
3. Voice & event debouncing to eliminate duplicate rapid triggers.
"""

import time
import functools
import threading
from collections import defaultdict
from typing import Dict, List, Callable, Optional
from flask import request, jsonify, make_response


class SlidingWindowRateLimiter:
    """Thread-safe sliding window rate limiter tracking request timestamps per client key (e.g. IP)."""

    def __init__(self, default_max_requests: int = 40, default_window_seconds: int = 60):
        self.default_max = default_max_requests
        self.default_window = default_window_seconds
        self.records: Dict[str, List[float]] = defaultdict(list)
        self.lock = threading.Lock()

    def is_allowed(self, key: str, max_requests: Optional[int] = None, window_seconds: Optional[int] = None) -> tuple[bool, int]:
        """
        Evaluates whether a request from `key` is permitted.
        Returns (is_allowed, retry_after_seconds).
        """
        max_req = max_requests if max_requests is not None else self.default_max
        win_sec = window_seconds if window_seconds is not None else self.default_window
        now = time.time()
        cutoff = now - win_sec

        with self.lock:
            # Purge expired timestamps outside current window
            valid_timestamps = [t for t in self.records[key] if t > cutoff]
            self.records[key] = valid_timestamps

            if len(valid_timestamps) >= max_req:
                oldest_in_window = valid_timestamps[0]
                retry_after = max(1, int(oldest_in_window + win_sec - now))
                return False, retry_after

            # Record current timestamp
            self.records[key].append(now)
            return True, 0


# Global limiter instance
flask_limiter = SlidingWindowRateLimiter(default_max_requests=40, default_window_seconds=60)


def rate_limit(max_requests: int = 40, window_seconds: int = 60):
    """
    Flask route decorator for enforcing sliding-window rate limits.
    Returns HTTP 429 with 'Retry-After' header if exceeded.
    """
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            # Extract client IP (supporting X-Forwarded-For if proxied)
            client_ip = request.headers.get('X-Forwarded-For', request.remote_addr or '127.0.0.1')
            if ',' in client_ip:
                client_ip = client_ip.split(',')[0].strip()

            key = f"{request.endpoint or fn.__name__}:{client_ip}"
            allowed, retry_after = flask_limiter.is_allowed(key, max_requests, window_seconds)

            if not allowed:
                resp = make_response(
                    jsonify({
                        "error": "Rate limit exceeded. Too many requests.",
                        "status": 429,
                        "retry_after_seconds": retry_after
                    }),
                    429
                )
                resp.headers["Retry-After"] = str(retry_after)
                return resp

            return fn(*args, **kwargs)
        return wrapper
    return decorator


class OutgoingThrottler:
    """Throttles outgoing external API requests to prevent bursting and 429 errors."""

    def __init__(self, min_interval_seconds: float = 0.3):
        self.min_interval = min_interval_seconds
        self.last_called: Dict[str, float] = {}
        self.lock = threading.Lock()

    def wait(self, service_name: str = "default"):
        """Blocks for remainder of min_interval if called too rapidly."""
        with self.lock:
            now = time.time()
            last = self.last_called.get(service_name, 0.0)
            elapsed = now - last
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            self.last_called[service_name] = time.time()


api_throttler = OutgoingThrottler(min_interval_seconds=0.3)


def exponential_backoff(max_retries: int = 3, base_delay: float = 1.0, factor: float = 2.0):
    """
    Decorator for retrying unstable network calls with exponential backoff.
    """
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            delay = base_delay
            last_err = None
            for attempt in range(1, max_retries + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_err = e
                    if attempt == max_retries:
                        raise e
                    time.sleep(delay)
                    delay *= factor
            raise last_err
        return wrapper
    return decorator


class DebounceCooldown:
    """Debounces rapid duplicate events (e.g. repeated audio triggers)."""

    def __init__(self, cooldown_seconds: float = 0.5):
        self.cooldown = cooldown_seconds
        self.last_time: Dict[str, float] = {}
        self.lock = threading.Lock()

    def should_process(self, key: str = "voice") -> bool:
        """Returns True if cooldown has elapsed since the last accepted trigger."""
        with self.lock:
            now = time.time()
            last = self.last_time.get(key, 0.0)
            if now - last < self.cooldown:
                return False
            self.last_time[key] = now
            return True


voice_debouncer = DebounceCooldown(cooldown_seconds=0.5)
