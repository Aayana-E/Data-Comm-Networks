from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)

AS_IP = "10.9.10.2"  
AS_PORT = 53533  #Server Port

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    hostname = request.args.get('hostname')
    number = request.args.get('number')

    if not hostname or not number:
        return jsonify({"error": "Missing parameters"}), 400

    dns_query = f"TYPE=A\nNAME={hostname}\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(dns_query.encode(), (AS_IP, AS_PORT))
    response, _ = sock.recvfrom(1024)
    sock.close()

    response_data = response.decode().split("\n")
    ip_address = None
    for line in response_data:
        if line.startswith("VALUE="):
            ip_address = line.split("=")[1]

    if not ip_address:
        return jsonify({"error": "Hostname not found"}), 404

    #Forward request
    fib_url = f"http://{ip_address}:9090/fibonacci?number={number}"
    fib_response = requests.get(fib_url)

    return (fib_response.text, fib_response.status_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
