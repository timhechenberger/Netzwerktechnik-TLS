
# TLs ohne mTLS

import socket
import ssl

HOST, PORT = "127.0.0.1", 8443

# TLS-Server-Kontext
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.minimum_version = ssl.TLSVersion.TLSv1_2

# Server-Zertifikat + Key laden
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# CA-Zertifikat laden
context.load_verify_locations(cafile="ca.crt")

# Für mTLS später:
# context.verify_mode = ssl.CERT_REQUIRED

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"TLS Server running at https://{HOST}:{PORT}")

    while True:
        raw_conn, addr = sock.accept()
        try:
            with context.wrap_socket(raw_conn, server_side=True) as conn:
                print("TLS connection established with:", addr, "via", conn.version())
                data = conn.recv(4096)
                if not data:
                    continue
                print("Received (encrypted on wire):", data)
                conn.sendall(b"echo: " + data)
        except ssl.SSLError as e:
            print("TLS Error:", e)


"""
# Code für mit mTLS
import socket
import ssl

HOST, PORT = "127.0.0.1", 8443

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.minimum_version = ssl.TLSVersion.TLSv1_2

# Server-Zertifikat
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# CA, der wir für Client-Zertifikate vertrauen
context.load_verify_locations(cafile="ca.crt")

# WICHTIG: Client-Zertifikat verpflichtend → mTLS
context.verify_mode = ssl.CERT_REQUIRED

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"mTLS Server running at https://{HOST}:{PORT}")

    while True:
        raw_conn, addr = sock.accept()
        try:
            with context.wrap_socket(raw_conn, server_side=True) as conn:
                print("mTLS connection established with:", addr, "via", conn.version())

                # Optional: Client-Zertifikat anzeigen
                cert = conn.getpeercert()
                print("Client certificate subject:", cert.get("subject"))

                data = conn.recv(4096)
                if not data:
                    continue
                conn.sendall(b"echo: " + data)
        except ssl.SSLError as e:
            print("TLS Error:", e)
"""


