import socketserver, threading, struct, os, pickle, sqlite3
def connect(filename):
	create = not os.path.exists(filename)
	db = sqlite3.connect(filename)
	print (create)
	if create:
		cursor = db.cursor()
		cursor.execute("CREATE TABLE encodings("
			"id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,"
			"filename TEXT NOT NULL,"
			"encoding TEXT NOT NULL)")
		db.commit()
	return db
def main():
	global db
	db = connect('/home/sepatuu/peter/Network/UDloader/Server/Encodings/encodings.sql')
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
		global db
		if filename == 'UDloader_server.py' or filename in self.get_files():
			return 'cannot create file named \'{}\''.format(filename)
		try:
			with open('Files/' + filename, 'wb') as fh:
				if encode == None:
					fh.write(txt)
				else:
					fh.write(txt.encode(encoding=encode))
		except Exception as err:
			print ('UPLOAD ERROR:', err)
		cursor = db.cursor()
		cursor.execute("INSERT INTO encodings(filename, encoding) VALUES (?, ?)", (filename, str(encode)))
		db.commit()
		return ''
	def get_files(self):
		rvalue = []
		for ignore1, ignore2, filename in os.walk('Files'):
			rvalue += [filename]
		return rvalue
	def get_text(self, filename):
		global db
		cursor = db.cursor()
		cursor.execute("SELECT encoding "
			"FROM encodings "
			"WHERE filename=?", (filename,))
		encode = cursor.fetchone()[0]
		if encode == 'None':
			encode = None
		try:
			with open('Files/' + filename, 'rb') as fh:
				print (encode)
				if encode == None:
					text = fh.read()
				else:
					text = fh.read().decode(encoding=encode)
		except Exception as err:
			print ('GET TEXT ERROR:', err)
			return
		return text
Call = {'UPLOAD':lambda self, *args:self.upload(*args), \
	'GET_FILES':lambda self, *args:self.get_files(*args), \
	'GET_TEXT':lambda self, *args:self.get_text(*args)}
CallLock = threading.Lock()
main()
