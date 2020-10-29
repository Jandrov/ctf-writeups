from pwn import * # pip install pwntools

r = remote('155.138.239.104', 8888, level="debug")
line1 = r.recvline()[54:-1]
r.recv(23)
r.sendline(line1)
line2 = r.recvline()[31:-1]
r.recv(12)
r.sendline(line2)
r.recvline()
r.recvline()







