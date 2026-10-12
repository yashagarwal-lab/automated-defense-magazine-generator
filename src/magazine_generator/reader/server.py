import http.server
import socketserver
import os
import sys
from pathlib import Path

from ..config import OUTPUT_DIR, STATIC_DIR
from ..rendering.engine import render_web_reader, render_print_magazine

class MagazineReaderHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        # Strip query string
        clean_path = path.split("?", 1)[0]
        if clean_path in ("/", "/reader", "/reader.html"):
            return str(OUTPUT_DIR / "reader.html")
        elif clean_path in ("/print", "/index.html", "/print.html"):
            return str(OUTPUT_DIR / "index.html")
        elif clean_path.startswith("/images/"):
            return str(STATIC_DIR / clean_path.lstrip("/"))
        elif clean_path.startswith("/css/"):
            return str(STATIC_DIR / clean_path.lstrip("/"))
        elif clean_path.startswith("/js/"):
            return str(STATIC_DIR / clean_path.lstrip("/"))
        elif clean_path.startswith("/static/"):
            rel = clean_path.replace("/static/", "", 1)
            return str(STATIC_DIR / rel)
        return super().translate_path(path)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

def run_server(host: str = "127.0.0.1", port: int = 8000):
    """Run local preview server for digital flipbook reader and print view."""
    print_file = OUTPUT_DIR / "index.html"
    reader_file = OUTPUT_DIR / "reader.html"

    if not print_file.exists():
        print("Rendering print magazine HTML...")
        render_print_magazine(print_file)
    if not reader_file.exists():
        print("Rendering digital web reader HTML...")
        render_web_reader(reader_file)

    handler = MagazineReaderHandler
    with socketserver.TCPServer((host, port), handler) as httpd:
        print(f"📖 Automated Defense Magazine Server listening on http://{host}:{port}/")
        print(f"   - Digital Reader: http://{host}:{port}/reader")
        print(f"   - Print Layout:   http://{host}:{port}/print")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
