#!/usr/bin/env python3
"""Serve docs/ the way GitHub Pages will: under /mortice-tenon-site/ (preview path) and at /
(custom-domain path), with 404.html for missing files.

    python3 tools/serve.py [port]      # default 8765
"""
import functools
import http.server
import pathlib
import sys

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
PREFIX = "/mortice-tenon-site"


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        if path.startswith(PREFIX + "/") or path == PREFIX:
            path = path[len(PREFIX):] or "/"
        return super().translate_path(path)

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            body = (DOCS / "404.html").read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
            return
        super().send_error(code, message, explain)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    handler = functools.partial(Handler, directory=str(DOCS))
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as srv:
        print(f"http://127.0.0.1:{port}{PREFIX}/")
        srv.serve_forever()
