#Levin Ayrilmaz 2023 

#switch.py

import socket
import threading

def forward_messages(client_socket, server_socket, switch_event, client_id, switch_socket, monitor_mode, connected_clients):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            if not switch_event.is_set():
                if "-from" in data:
                        message, from_, client_id_spoof = data.split(" ", 3)
                        print(f'Received from client {client_id_spoof} -> {message}')
                        server_socket.send(f'{client_id_spoof}: {data}'.encode())
                else:
                    print(f'Received from client {client_id} -> {data}')
                    server_socket.send(f'{client_id}: {data}'.encode())

        except Exception as e:
            print(f"Error forwarding message from client {client_id} to server:", str(e))
            break





def receive_responses(client_socket, server_socket, switch_event):
    while True:
        try:
            data = server_socket.recv(1024).decode()
            if not data:
                break
            print('Received from server -> ' + data)

            if not switch_event.is_set():
                client_socket.send(data.encode())

        except Exception as e:
            print("Error receiving response from server -> ", str(e))
            break

def switch_program():
    switch_host = socket.gethostname()
    switch_port = int(input("Switch Port?: "))

    switch_socket = socket.socket()
    switch_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    switch_socket.bind((switch_host, switch_port))
    switch_socket.listen(2)

    print("Switch is ready to forward messages.")

    try:
        switch_event = threading.Event()
        monitor_mode = threading.Event()
        connected_clients = {}

        while True:
            client_socket, client_address = switch_socket.accept()
            print("Connection from client: " + str(client_address))

            client_id = client_socket.recv(1024).decode()
            print(f"ID for client {client_address}: {client_id}")

            server_socket = socket.socket()
            server_socket.connect((switch_host, 12345))
            server_socket.send(client_id.encode())
            print("Connected to the server.")

            connected_clients[client_id] = client_socket

            forward_thread = threading.Thread(target=forward_messages, args=(client_socket, server_socket, switch_event, client_id, switch_socket, monitor_mode, connected_clients))
            response_thread = threading.Thread(target=receive_responses, args=(client_socket, server_socket, switch_event))

            forward_thread.start()
            response_thread.start()

    finally:
        switch_socket.close()

if __name__ == '__main__':
    switch_program()
