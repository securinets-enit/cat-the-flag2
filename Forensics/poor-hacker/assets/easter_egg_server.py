#!/usr/bin/env python3
# ~/flag_server.py
from flask import Flask, request, jsonify, abort
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

EXPECTED_TOKEN = "SecurinetsENIT{837b8d424c0445ab3a51f1100da61a4b}"
FLAG = "SecurinetsENIT{d06076ce3a0f542bada9c84ed02f3cb8}"

@app.route("/", methods=["GET", "POST"])
def index():
    auth = request.headers.get("Authorization", "")
    app.logger.info("Incoming request from %s, auth=%s", request.remote_addr, auth[:80] if auth else "<none>")
    if not auth.startswith("Bearer "):
        abort(401, description="Missing Bearer token")
    token = auth[len("Bearer "):].strip()
    if token == EXPECTED_TOKEN:
        return jsonify({"flag": FLAG})
    else:
        abort(401, description="Invalid token")

if __name__ == "__main__":
    # Use cert.pem and key.pem in the same directory as this script
    basedir = os.path.dirname(os.path.realpath(__file__))
    cert = os.path.join(basedir, "cert.pem")
    key = os.path.join(basedir, "key.pem")
    if not (os.path.isfile(cert) and os.path.isfile(key)):
        raise SystemExit("cert.pem / key.pem not found in script directory.")
    # Bind to 0.0.0.0 for external access, port 4443 (non-privileged)
    app.run(host="0.0.0.0", port=443, ssl_context=(cert, key))

