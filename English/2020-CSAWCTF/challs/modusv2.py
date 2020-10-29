from pwn import * # pip install pwntools

flag = "0110011001101100011000010110011101111011"
modes = [b"ECB",b"CBC"]
i = 0

def recv_2_lines(r):
	try:
		r.recvline()
		r.recvline()
	except EOFError:
		print(flag)

errors = 0
n = len(flag)
while True:
	if errors == 2:
		print(flag)
		break

	r = remote('crypto.chal.csaw.io', 5001)

	recv_2_lines(r)
	for num in flag:
		r.sendline("")
		recv_2_lines(r)
		sent = modes[int(num)]
		r.sendline(sent)
		try:
			line = r.recvline()
		except EOFError:
			print(flag)
			break

	while True:
		r.sendline("")
		recv_2_lines(r)
		sent = modes[i]
		r.sendline(sent)
		try:
			line = r.recvline()
			flag += str(i)
			n += 1
			errors = 0
		except EOFError:
			i = (i + 1) % 2
			errors += 1
			print(n)
			break
		



