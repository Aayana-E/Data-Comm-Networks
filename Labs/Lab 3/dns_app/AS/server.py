import socket

AS_PORT = 53533
DNS_DB = {}

def handle_request(data):
    lines = data.decode().split("\n")
    request_type = lines[0].split("=")[1]

    if request_type == "A":
        if "VALUE=" in data.decode():  
            name = lines[1].split("=")[1]
            value = lines[2].split("=")[1]
            DNS_DB[name] = value
            return b"Registration Successful\n"

        else:  # Query
            name = lines[1].split("=")[1]
            if name in DNS_DB:
                response = f"TYPE=A\nNAME={name}\nVALUE={DNS_DB[name]}\nTTL=10\n"
                return response.encode()
            else:
                return b"Not Found\n"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", AS_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    response = handle_request(data)
    sock.sendto(response, addr)
