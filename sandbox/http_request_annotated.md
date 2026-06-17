# Exercise 13.11 part 1 — one raw HTTP request, annotated

Captured by `see_http.py` on 2026-06-12. My client was `curl` (Claude has no
graphical browser); visit with Chrome yourself and you'll see the same shape
with ~8 more headers — differences noted below.

## The request, byte for byte

```
GET / HTTP/1.1
Host: 127.0.0.1:8000
User-Agent: curl/8.19.0
Accept: */*

```

## Line by line

**`GET / HTTP/1.1` — the request line.**
- Method: `GET` — "read something, change nothing." No body follows (that's
  why the request simply ends after the blank line).
- Path: `/` — the site root. I typed no path after the port, so the client
  filled in the default. The server never sees `http://127.0.0.1:8000` —
  the address was used to *open the pipe*; only the path travels *inside* it.
- `HTTP/1.1` — which dialect of the protocol we're speaking.

**`Host: 127.0.0.1:8000`** — "which site I meant." Looks redundant (we just
connected there!) but one server at one IP can host fifty domains; this header
is how it knows which one to serve. It's the only *mandatory* header in
HTTP/1.1 — a request without it gets rejected by real servers.

**`User-Agent: curl/8.19.0`** — "who's asking," software-wise. Pure
self-identification: servers use it for stats and workarounds, nothing
enforces honesty (curl can claim to be Chrome with one flag — it's a
business card, not a passport). In your browser this reads
`Mozilla/5.0 (Windows NT 10.0; Win64; x64) ... Chrome/...`.

**`Accept: */*`** — "what formats I can handle." `*/*` = "anything, I'm not
picky" (curl just saves bytes). Chrome sends a ranked wish-list instead
(`text/html,application/xhtml+xml,...;q=0.9`) so servers that can produce
multiple formats know to prefer HTML. This is the request-side twin of the
response's `Content-Type`.

**The blank line** — end of headers, and since GET has no body, end of
request. The earlier "ghost request" from Invoke-WebRequest also carried
`Connection: Keep-Alive` — "leave the pipe open, I may ask again" — the
default in HTTP/1.1; browsers send it (or rely on it) to avoid re-opening
a connection per image/css/js file.

## What a browser adds that curl doesn't

Cookie headers (session identity — Module 6), `Accept-Encoding: gzip`
("compress it, I can unzip"), `Accept-Language: es-CO` (yes, it leaks your
locale), and a `favicon.ico` follow-up request you never asked for.
