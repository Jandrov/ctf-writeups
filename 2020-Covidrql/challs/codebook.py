#!/usr/bin/python3
import os
import random
import socket
import string
import sys
import threading

from Crypto.Cipher import AES


FLAG = b'DUMMY_FLAG'


def connection(conn):
    try:
        conn.settimeout(2)
        key = os.urandom(16)
        passphrase = ''.join([random.choice(string.ascii_letters) for _ in range(32)])
        cipher = AES.new(key, AES.MODE_ECB)
        
        enc_passphrase = cipher.encrypt(
                    f'Passphrase  is  {passphrase}'.encode()
                ).hex()

        conn.send(
                f'Encrypted passphrase: {enc_passphrase}\n'.encode()
            )
        conn.send(b'Message to decrypt (64 bytes max): ')
        enc_msg = conn.recv(1024).decode().replace('\n', '')
        if len(enc_msg) > 64:
            raise Exception('Message too long')

        msg = cipher.decrypt(bytes.fromhex(enc_msg)).decode()
        conn.send(f'Decrypted message: {msg}\n'.encode())
        conn.send(b'Passphrase: ')
        pp = conn.recv(1024).decode().replace('\n', '')
        if pp == passphrase:
            conn.send(b'Correct passphrase!\n')
            conn.send(f'Flag: {FLAG}\n'.encode())

        else:
            conn.send(b'Incorrect passphrase\n')

        conn.close()

    except Exception as exn:
        conn.send(exn.__str__().encode())

    finally:
        conn.close()


if __name__ == '__main__':
    PORT = int(sys.argv[1])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('0.0.0.0', PORT))
        sock.listen()
        while True:
            conn, addr = sock.accept()
            threading.Thread(target=connection, args=(conn,)).start()

    finally:
        sock.close()

