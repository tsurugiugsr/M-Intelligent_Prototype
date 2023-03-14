import socket
import modules.MLinking.protobuf.protobuflink as protolink
from flask import Flask, request

def Server_Intelli_Http():
    host_Intelli_Http = ''
    port_Intelli_Http = 211
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((host_Intelli_Http, port_Intelli_Http))
    listen_socket.listen(1)
    print('Serving HTTP on port %s ...' % port_Intelli_Http)
    while True:
        try:
            client_connection, client_address = listen_socket.accept()
            request = client_connection.recv(10240)
            print(request.decode())
            protolink.parse_Request(request)

            http_response = """\
HTTP/1.1 200 OK

Hello, World!
"""
            client_connection.sendall(http_response.encode("utf-8"))
            client_connection.close()
        finally:
            pass



app = Flask(__name__)
BASE_URL = '/audio2bs'

@app.route(BASE_URL, methods=['POST'])
def post():

    data = request.get_data()
    print(type(data))
    print(data)
    requestContent, requestTTSType = protolink.parse_Request(data)
    
    return protolink.encode_Response(requestContent, requestTTSType)
    
def ServerFlask_Intelli_Http():
    app.run(debug=True, host='0.0.0.0', port=211)

