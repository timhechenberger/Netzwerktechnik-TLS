import socket

HOST, PORT = "127.0.0.1", 8443  # gleich wie bei TLS

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"Plain TCP Server running at {HOST}:{PORT}")

    while True:
        conn, addr = sock.accept()
        with conn:
            print("Connection from:", addr)
            data = conn.recv(4096)
            if not data:
                continue
            print("Received:", data)
            conn.sendall(b"echo: " + data)