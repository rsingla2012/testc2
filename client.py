import socket
import getpass

SERVER_IP = '172.30.168.4'
SERVER_PORT = 2002

def connect_and_authenticate():
    sock = socket.socket()
    sock.connect((SERVER_IP, SERVER_PORT))
    print("[+] Connected to server")

    password = getpass.getpass("Enter session password: ")
    sock.sendall(password.encode())

    return sock

def command_loop(sock):
    try:
        while True:
            cmd = input("Shell> ").strip()
            if not cmd:
                continue
            if cmd.lower() == 'exit':
                sock.close()
                break

            sock.sendall(cmd.encode())
            result = sock.recv(4096).decode()
            print(result)

    except Exception as ex:
        print(f"[-] Connection lost: {ex}")
        sock.close()

if __name__ == "__main__":
    client_socket = connect_and_authenticate()
    command_loop(client_socket)
