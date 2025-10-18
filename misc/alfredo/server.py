#!/usr/bin/env python3
# flag_server_head.py
# HTTP server that ONLY accepts HEAD requests.
# It responds with many custom headers. The flag is in the header named "L3alam bidou".
#
# Usage:
#   python3 flag_server_head.py [PORT]
# Example:
#   python3 flag_server_head.py 31337

import http.server
import socketserver
import sys

# The exact flag value you requested
FLAG = "Securinets_fst{8ea0117cab55c2cfa9e9ce4e7d6b16f9}"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 31337

class Handler(http.server.SimpleHTTPRequestHandler):
    server_version = "SecurinetsENIT-HeadServer/1.0"

    # central place to add many custom headers (called for any response)
    def end_headers(self):
        # The requested header (name includes a space as you asked)
        # Value is the flag
        self.send_header("L3alam bidou", FLAG)

        # lots of additional innocuous / custom headers to blend the flag in
        self.send_header("X-Securinets-Mode", "production")
        self.send_header("X-Server-Region", "eu-west-1")
        self.send_header("X-RateLimit-Remaining", "4999")
        self.send_header("X-Request-ID", "req-7f4a2b8c")
        self.send_header("X-Powered-By", "Python3")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Cache-Status", "HIT")
        self.send_header("X-Feature-Flag-Alpha", "enabled")
        self.send_header("X-Feature-Flag-Beta", "disabled")
        self.send_header("X-Custom-Note", "Lwaywa ettounsi")
        self.send_header("Server", self.server_version)
        # always call the base implementation last
        super().end_headers()

    # Only allow HEAD. For HEAD, send headers but no body.
    def do_HEAD(self):
        self.send_response(200)
        # Content-Type and Content-Length are still useful for HEAD
        self.send_header("Content-Type", "text/html; charset=utf-8")
        # indicate zero body length for HEAD responses
        self.send_header("Content-Length", "0")
        # end_headers will add the custom headers (including the flag)
        self.end_headers()

    # Reject GET / POST / others with 405
    def do_GET(self):
        self.send_error(405, "Who is Alfredo Garcia and why the f*ck would I bring you his HEAD.")

    def do_POST(self):
        self.send_error(405, "NON.")

    def do_PUT(self):
        self.send_error(405, "NON.")

    def do_DELETE(self):
        self.send_error(405, "BJEH RABI ALEH DELETE.")

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"[+] Serving on port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[+] Shutting down")
            httpd.server_close()

