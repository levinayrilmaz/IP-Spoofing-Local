#Levin Ayrilmaz 2023

#server.py

import socket
import threading


client_tokens = {}
switch_event = threading.Event() 

def handle_client(conn, address):
    print("Connection from: " + str(address))
    client_id = str(conn.recv(1024).decode())
    client_tokens[client_id] = (conn, address)

    print(f"ID for {address}: {client_id}")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        if "-from" in data:
            _, message, from_, client_id_spoof = data.split(" ", 3)
            send_response(client_tokens[client_id_spoof], message, client_id_spoof)
        else:
            send_response(client_tokens[client_id], data.split(" ")[1], client_id)

    conn.close()


def send_response(client_data, message, client_id):
    conn, address = client_data
    print("Sending to client {}: {}".format(client_id, message))
    response = f"Response for {client_id}: {message}"
    conn.send(response.encode())

def server_program():
    host = socket.gethostname()
    port = 12345

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(2)

    print("Server is ready to receive connections. (Port="+str(port)+")")

    try:
        while True:
            conn, address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(conn, address))
            client_handler.start()
    finally:
        server_socket.close()

if __name__ == '__main__':
    server_program()
