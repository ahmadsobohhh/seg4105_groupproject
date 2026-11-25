"""Local prototype for reviewing suggested software bug triage."""

import json
import os
import re
import sqlite3
from contextlib import closing
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
DATABASE = Path(os.environ.get("TRIAGE_DB", ROOT / "data" / "triage.sqlite3"))
PAGE = (ROOT / "index.html").read_bytes()
MAX_BODY = 24_000
CATEGORIES = (
    ("Authentication", "Identity", {"login", "password", "session", "signin", "sso"}),
    ("Interface", "Frontend", {"button", "layout", "page", "screen", "ui"}),
    ("Data", "Data Platform", {"database", "export", "import", "sync", "query"}),
    ("Reliability", "Platform", {"crash", "outage", "timeout", "unavailable", "latency"}),
)
CRITICAL = {"outage", "unavailable", "data loss", "cannot access"}
HIGH = {"crash", "timeout", "blocked"}
STOP_WORDS = {"the", "and", "when", "from", "this", "that", "with", "after"}


def words(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP_WORDS


def similarity(left, right):
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def recommend(title, description, previous):
    text = f"{title} {description}".lower()
    tokens = words(text)
    category, team = "General", "Triage Queue"
    best = 0
    for candidate, owner, keywords in CATEGORIES:
        score = len(tokens & keywords)
        if score > best:
            category, team, best = candidate, owner, score

    severity = "Medium"
    if tokens & CRITICAL or any(phrase in text for phrase in CRITICAL if " " in phrase):
        severity = "Critical"
    elif tokens & HIGH:
        severity = "High"

    title_tokens = words(title)
    matches = [
        (similarity(title_tokens, words(old_title)), report_id, old_title)
        for report_id, old_title in previous
    ]
    score, duplicate_id, duplicate_title = max(matches, default=(0.0, 0, ""))
    duplicate = {"id": duplicate_id, "title": duplicate_title} if score >= 0.7 else None
    summary = re.sub(r"\s+", " ", description).strip()
    if len(summary) > 180:
        summary = summary[:177].rstrip() + "..."
    return {
        "category": category,
        "severity": severity,
        "team": team,
        "summary": summary,
        "possible_duplicate": duplicate,
    }


def init_database():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(DATABASE)) as db, db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                recommendation TEXT NOT NULL
            )
        """)


def save_report(title, description):
    with closing(sqlite3.connect(DATABASE)) as db, db:
        db.execute("BEGIN IMMEDIATE")
        previous = db.execute(
            "SELECT id, title FROM reports ORDER BY id DESC LIMIT 100"
        ).fetchall()
        result = recommend(title, description, previous)
        cursor = db.execute(
            "INSERT INTO reports (title, description, recommendation) VALUES (?, ?, ?)",
            (title, description, json.dumps(result)),
        )
        return {"id": cursor.lastrowid, "title": title, **result}


class Handler(BaseHTTPRequestHandler):
    def send_body(self, status, content_type, body):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, status, value):
        self.send_body(status, "application/json", json.dumps(value).encode("utf-8"))

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/":
            self.send_body(200, "text/html; charset=utf-8", PAGE)
        elif path == "/health":
            self.send_json(200, {"status": "ok"})
        else:
            self.send_json(404, {"error": "Route not found."})

    def do_POST(self):
        if urlsplit(self.path).path != "/api/reports":
            self.send_json(404, {"error": "Route not found."})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_json(400, {"error": "Invalid request size."})
            return
        if size < 1 or size > MAX_BODY:
            self.send_json(413, {"error": "Request size is outside the accepted range."})
            return
        try:
            payload = json.loads(self.rfile.read(size))
            title = payload.get("title", "")
            description = payload.get("description", "")
            if not isinstance(title, str) or not isinstance(description, str):
                raise ValueError
            title, description = title.strip(), description.strip()
            if not 1 <= len(title) <= 160 or not 1 <= len(description) <= 4000:
                raise ValueError
        except (ValueError, AttributeError):
            self.send_json(400, {"error": "Enter a title and a description within the limits."})
            return
        self.send_json(201, save_report(title, description))


if __name__ == "__main__":
    init_database()
    with ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), Handler) as server:
        server.serve_forever()
