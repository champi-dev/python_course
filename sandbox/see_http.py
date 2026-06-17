import socket

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 8000))
server.listen()
print("Listening on http://127.0.0.1:8000 — visit it in your browser...")

conn, addr = server.accept()
request = conn.recv(4096).decode()
print("=" * 60)
print(request)
print("=" * 60)

body = "<h1>Got it. Now look at your terminal.</h1>"
response = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html; charset=utf-8\r\n"
    f"Content-Length: {len(body.encode())}\r\n"
    "\r\n"
    + body
)
conn.sendall(response.encode())
conn.close()
server.close()
