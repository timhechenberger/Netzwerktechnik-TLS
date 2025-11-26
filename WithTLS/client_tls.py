


# Etwas umgestalter Code für mTLS
import socket
import ssl

HOST, PORT = "localhost", 8443

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.minimum_version = ssl.TLSVersion.TLSv1_2

# CA, der wir für den SERVER vertrauen
context.load_verify_locations(cafile="ca.crt")

# NEU: Client-Zertifikat + Key für mTLS
context.load_cert_chain(certfile="client.crt", keyfile="client.key")

with socket.create_connection((HOST, PORT)) as raw_sock:
    with context.wrap_socket(raw_sock, server_hostname="localhost") as conn:
        print("mTLS connection established, protocol:", conn.version())
        msg = b"hello mtls"
        conn.sendall(msg)
        print("Sent:", msg)
        resp = conn.recv(4096)
        print("Response:", resp.decode("utf-8", errors="replace"))
