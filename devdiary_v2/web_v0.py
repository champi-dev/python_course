import html
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

from devdiary.models import EntryLog

DATA_PATH = Path("devdiary.json")

KNOWN_PATHS = ("/", "/stats", "/entry/<n>")


def esc(text: str) -> str:
    return html.escape(text)


def page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html><body>
  <h1>{title}</h1>
  {body}
  <p><a href="/">home</a> &middot; <a href="/stats">stats</a></p>
</body></html>"""


def render_home(log: EntryLog) -> str:
    items = "".join(
        f'<li><a href="/entry/{i}">{esc(e.topic)}</a> — '
        f"{e.minutes} min ({e.mood})</li>"
        for i, e in enumerate(log, start=1)
    )
    intro = f"<p>{len(log)} entries — current streak {log.streak()} day(s)</p>"
    return page("DevDiary", intro + f"<ul>{items or '<li>(no entries yet)</li>'}</ul>")


def render_stats(log: EntryLog) -> str:
    if not log:
        return page("DevDiary — stats", "<p>(no entries yet)</p>")
    s = log.stats()
    body = (
        f"<p>Entries: {s['count']}</p>"
        f"<p>Total time: {s['total_minutes']} min "
        f"(~{s['total_minutes'] / 60:.1f} hr)</p>"
        f"<p>Average: {s['average']:.1f} min/entry</p>"
        f"<p>Longest: {esc(s['longest'].topic)} ({s['longest'].minutes} min)</p>"
        f"<p>Current streak: {log.streak()} day(s)</p>"
    )
    return page("DevDiary — stats", body)


def render_entry(entry, number: int) -> str:
    when = entry.created_at.strftime("%Y-%m-%d %H:%M")
    return page(
        f"DevDiary — entry {number}",
        f"<p><b>{esc(entry.topic)}</b></p>"
        f"<p>{entry.minutes} min, mood {entry.mood}, logged {when}</p>",
    )


def render_404() -> str:
    links = "".join(f"<li><code>{esc(p)}</code></li>" for p in KNOWN_PATHS)
    return page("404 — nothing lives here", f"<p>Paths that do exist:</p><ul>{links}</ul>")


class DevDiaryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        log = EntryLog.load(DATA_PATH)
        if self.path == "/":
            self.respond(200, render_home(log))
        elif self.path == "/stats":
            self.respond(200, render_stats(log))
        elif self.path.startswith("/entry/"):
            self.entry_route(log)
        else:
            self.respond(404, render_404())

    def entry_route(self, log: EntryLog) -> None:
        try:
            number = int(self.path.removeprefix("/entry/"))
            if number < 1:
                raise IndexError
            entry = log.entries[number - 1]
        except (ValueError, IndexError):
            self.respond(404, render_404())
            return
        self.respond(200, render_entry(entry, number))

    def respond(self, status: int, html_text: str) -> None:
        body = html_text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), DevDiaryHandler)
    print("DevDiary on http://127.0.0.1:8000 — Ctrl+C to stop")
    server.serve_forever()
