#Levin Ayrilmaz 2023

#client.py

import socket
import threading

def start():
    id = input("ID (192.168.0.XX): ")
    client_program(id)

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print('Received from server -> ' + data)
        except Exception as e:
            print("Error receiving message -> ", str(e))
            break

def client_program(id):
    host = socket.gethostname()
    port = int(input("Switch Port?: "))

    client_socket = socket.socket()
    client_socket.connect((host, port))

    client_socket.send(id.encode())

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()

        if message.lower().strip() == 'bye':
            break

        else:
            try:
                client_socket.send(message.encode())
            except Exception as e:
                print("Error sending message:", str(e))
                break

    client_socket.close()

if __name__ == '__main__':
    start()
