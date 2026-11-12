#!/usr/bin/env python3
"""Minimal HTTP service exposing health checks and Prometheus metrics."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock
import os
import time

STARTED = time.time()
LOCK = Lock()
REQUESTS = 0


class Handler(BaseHTTPRequestHandler):
    server_version = "ReliabilityLab/1.0"

    def do_GET(self) -> None:
        global REQUESTS
        with LOCK:
            REQUESTS += 1
            count = REQUESTS
        if self.path == "/healthz":
            self._send(200, "ok\n", "text/plain; charset=utf-8")
        elif self.path == "/readyz":
            self._send(200, "ready\n", "text/plain; charset=utf-8")
        elif self.path == "/metrics":
            body = (
                "# HELP reliability_lab_requests_total Total HTTP requests handled.\n"
                "# TYPE reliability_lab_requests_total counter\n"
                f"reliability_lab_requests_total {count}\n"
                "# HELP reliability_lab_uptime_seconds Process uptime in seconds.\n"
                "# TYPE reliability_lab_uptime_seconds gauge\n"
                f"reliability_lab_uptime_seconds {time.time() - STARTED:.2f}\n"
            )
            self._send(200, body, "text/plain; version=0.0.4; charset=utf-8")
        elif self.path == "/":
            self._send(200, "container reliability lab\n", "text/plain; charset=utf-8")
        else:
            self._send(404, "not found\n", "text/plain; charset=utf-8")

    def _send(self, status: int, body: str, content_type: str) -> None:
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"{self.address_string()} - {fmt % args}", flush=True)


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8080"))
    ThreadingHTTPServer((host, port), Handler).serve_forever()
