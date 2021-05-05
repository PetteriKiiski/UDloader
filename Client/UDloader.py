import socket, sys, struct, pickle, os
Address = ('10.0.0.147', 9653)
def main():
	options = {'u':upload, 'd':download, 'r':read, 'e':exit}
	while True:
		option = input('(U)pload (D)ownload (R)ead (E)xit: ')
		try:
			options[option]()
		except KeyError:
			print ('That wasn\'t an option')
def upload():
	filename = input('which file do you want to upload?: ')
	if not filename:
		return
	dir = input('what is the directory?')
	if not dir:
		dir = '.'
	if dir.startswith('~/'):
		dir = '/home/sepatuu' + dir[1:]
	try:
		with open(dir + '/' + filename, 'rb') as fh:
			txt = fh.read().decode(encoding='UTF-8')
	except EnvironmentError:
		print ('There was no such file')
		return
	print (handle_request('UPLOAD', filename, txt))
def download():
	filenames = handle_request('GET_FILES')
	print ('these are the available files:')
	for fn in filenames:
		print (fn)
	filename = input('which one do you chose: ')
	if not filename:
		return
	txt = handle_request('GET_TEXT', filename)
	print (txt)
	if txt is None:
		print ('You did not enter a correct filename')
		return
	try:
		with open('/home/sepatuu/Downloads/' + filename, 'wb') as fh:
			fh.write(txt.encode(encoding='UTF-8'))
	except EnvironmentError as err:
		print ('We have a problem in the downloading process:', err)
		return
def read():
	filenames = handle_request('GET_FILES')
	print ('these are the available files:')
	for fn in filenames:
		print (fn)
	filename = input('which one do you chose')
	if not filename:
		return
	txt = handle_request('GET_TEXT', filename)
	if txt is None:
		print ('You did not enter a correct filename')
		return
	print ()
	print (txt)
	print ()
def exit():
	print ('Goodbye!')
	sys.exit()
def handle_request(*info):
	SizeStruct = struct.Struct('!I')
	data = pickle.dumps(info, 3)
	print (pickle.loads(data))
	try:
		with SocketManager(Address) as sock:
			sock.sendall(SizeStruct.pack(len(data)))
			sock.sendall(data)
			size_data = sock.recv(SizeStruct.size)
			size = SizeStruct.unpack(size_data)
			size = size[0]
			result = bytearray()
			while True:
				data = sock.recv(4000)
				if not data:
					break
				result.extend(data)
				if len(result) >= size:
					break
	except socket.error as err:
		print ('ERROR:', err)
		sys.exit(1)
	return pickle.loads(result)
class SocketManager:
	def __init__(self, address):
		self.address = address
	def __enter__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect(self.address)
		return self.sock
	def __exit__(self, *ignore):
		self.sock.close()
main()
