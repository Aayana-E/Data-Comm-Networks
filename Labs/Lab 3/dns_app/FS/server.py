from flask import Flask, request, jsonify
import json
import socket

app = Flask(__name__)

FS_IP = "172.18.0.2"  #Fibonacci Server IP
AS_IP = "10.9.10.2"   #Authoritative Server IP
AS_PORT = 53533       #Authoritative Server Port

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

@app.route('/register', methods=['PUT'])
def register():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    hostname = data.get("hostname")
    ip = data.get("ip")

    if not hostname or not ip:
        return jsonify({"error": "Missing fields"}), 400

    
    dns_message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(dns_message.encode(), (AS_IP, AS_PORT))
    sock.close()

    return jsonify({"message": "Registered successfully"}), 201

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number')

    if not number.isdigit():
        return jsonify({"error": "Invalid number"}), 400

    result = fibonacci(int(number))
    return jsonify({"fibonacci": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
