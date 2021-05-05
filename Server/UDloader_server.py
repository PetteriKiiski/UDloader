import socketserver, threading, struct, os, pickle, sqlite3
def main():
	try:
		server = UDloaderServer(('10.0.0.147', 9653), RequestHandler)
		server.serve_forever()
	except Exception as err:
		print ('MAIN ERROR:', err)
	finally:
		if server is not None:
			server.shutdown()
class UDloaderServer(socketserver.TCPServer, socketserver.ThreadingMixIn):pass
class RequestHandler(socketserver.StreamRequestHandler):
	def handle(self):
		SizeStruct = struct.Struct('!I')
		size_data = self.rfile.read(SizeStruct.size)
		size = SizeStruct.unpack(size_data)
		size = size[0]
		info = self.rfile.read(size)
		info = pickle.loads(info)
#		print ([self, *info[1:]])
#		print (len([self, *info[1:]]))
#		print (info)
		with CallLock:
#			print (Call[info[0]])
			rvalue = Call[info[0]](self, *info[1:])
#			print (rvalue)
		response = pickle.dumps(rvalue, 3)
		self.wfile.write(SizeStruct.pack(len(response)))
		self.wfile.write(response)
	def upload(self, filename, txt, encode):
		if filename == 'UDloader_server.py' or filename in self.get_files():
			return 'cannot create file named \'{}\''.format(filename)
		try:
			with open(filename, 'wb') as fh:
				if encode == None:
					fh.write(txt)
				else:
					fh.write(txt.encode(encoding=encode))
		except Exception as err:
			print ('UPLOAD ERROR:', err)
		try:
			with open('/home/sepatuu/peter/Network/UDloader/Server/Encodings/encodings.dat', 'wb') as fh:
				fh.write('{0}={1}'.encode(encoding='UTF-8').format(filename, str(encode)))
		except Exception as err:
			print ('UPLOAD ERROR:', err)
		return ''
	def get_files(self):
		rvalue = []
		for ignore1, ignore2, filename in os.walk('.'):
			if filename == 'UDloader_server.py':
				continue
			rvalue += [filename]
		return rvalue
	def get_text(self, filename):
		try:
			with open(filename, 'rb') as fh:
				text = fh.read().decode(encoding='UTF-8')
		except Exception as err:
			print ('GET TEXT ERROR:', err)
		print (text)
		return text
Call = {'UPLOAD':lambda self, *args:self.upload(*args), \
	'GET_FILES':lambda self, *args:self.get_files(*args), \
	'GET_TEXT':lambda self, *args:self.get_text(*args)}
CallLock = threading.Lock()
main()
