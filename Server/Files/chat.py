import socket, sys, struct, pickle
Address = ('10.0.0.147', 9653)
def main():
	other_online = handle_request('IS_ONLINE', 1)
	print ('Lilja is', 'not' if not other_online else '', 'online')
	handle_request('ONLINE', 0, True)
	while True:
		text = input('Peter:')
		if text == 'exit' and 'y' in input('do you want to leave?: '):
			break
			handle_request('ONLINE', 0, False)
		if handle_request('IS_ONLINE', 1) != other_online:
			other_online = handle_request('IS_ONLINE', 1)
			print ('Lilja is', 'not' if not other_online else '', 'online')
		if text != '':
			handle_request('WRITE', text, 'PeterK')
		for chat in handle_request('READ', 'PeterK'):
			print ('Lilja:', chat)
def handle_request(*data):
	SizeStruct = struct.Struct('!I')
	info = pickle.dumps(data)
	try:
		with SocketManager(Address) as sock:
			sock.sendall(SizeStruct.pack(len(info)))
			sock.sendall(info)
			size_info = sock.recv(SizeStruct.size)
			size = SizeStruct.unpack(size_info)
			rval = sock.recv(size[0])
		return pickle.loads(rval)
	except socket.error as err:
		print (err)
		sys.exit(1)
class SocketManager:
	def __init__(self, address):
		self.address = address
	def __enter__(self, *ignore):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect(self.address)
		return self.sock
	def __exit__(self, *ignore):
		self.sock.close()
main()
