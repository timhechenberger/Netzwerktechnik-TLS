import socket

HOST, PORT = "127.0.0.1", 8443

with socket.create_connection((HOST, PORT)) as conn:
    msg = b"hello plain tcp"
    conn.sendall(msg)
    print("Sent:", msg)
    resp = conn.recv(4096)
    print("Response:", resp.decode("utf-8", errors="replace"))
