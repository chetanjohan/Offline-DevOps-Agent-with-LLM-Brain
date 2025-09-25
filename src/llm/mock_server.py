"""Lightweight mock LLM HTTP server.

This server accepts POST /generate with JSON {"prompt": "..."} and returns
JSON {"text": "MOCKED: ..."}. It uses only the Python standard library so
it can be used in unit tests and CI without extra dependencies.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import argparse
import threading
from typing import Tuple


class MockLLMHandler(BaseHTTPRequestHandler):
    def _send_json(self, obj, code=200):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path != "/generate":
            self._send_json({"error": "not found"}, code=404)
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""
        try:
            payload = json.loads(body.decode("utf-8"))
            prompt = payload.get("prompt", "")
        except Exception:
            self._send_json({"error": "invalid json"}, code=400)
            return

        # Simple mocked response
        resp = {"text": f"MOCKED: {prompt}"}
        self._send_json(resp)

    def log_message(self, format, *args):
        # Silence default logging to keep test output clean
        return


def run_server(host: str = "127.0.0.1", port: int = 8765, block: bool = True) -> Tuple[HTTPServer, threading.Thread]:
    server = HTTPServer((host, port), MockLLMHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    if block:
        try:
            thread.join()
        except KeyboardInterrupt:
            pass
    return server, thread


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    print(f"Starting mock LLM server on {args.host}:{args.port}")
    server, thread = run_server(args.host, args.port, block=True)


if __name__ == "__main__":
    main()
