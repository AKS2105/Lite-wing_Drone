import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5000))

print("Waiting for LiteWing telemetry...")

while True:
    data, addr = sock.recvfrom(1024)

    decoded = data.decode()

    print(decoded)

    with open("data.txt", "w") as f:
        f.write(decoded)