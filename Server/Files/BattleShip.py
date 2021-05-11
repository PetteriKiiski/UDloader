from tkinter import *
class Game:
	def __init__(self):
		self.tk = Tk()
		self.tk.resizable(0,0)
		self.tk.wm_attributes('-topmost', 1)
		self.canvas = Canvas(self.tk, width=600, height=500)
		self.canvas_width = 600
		self.canvas_height = 500
		self.canvas.pack()
		self.taken = []
		self.grid = []
		for x in range(50, 600, 50):
			self.grid.append([])
			for y in range(0, 550, 50):
				self.grid[len(self.grid)-1].append(GridSquare(self, x, y))
		self.tk.update()
	def mainloop(self):
		while True:
			self.tk.update()
			self.tk.update_idletasks()
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
class Coords:
	def __init__(self, x1=0, y1=0, x2=0, y2=0):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
	def __contains__(self, point):
		if point.x <= self.x2 and point.x >= self.x1 and point.y <= self.y2 and point.y >= self.y1:
			return True
		return False
class Sprite:
	def __init__(self, game):
		self.game = game
		self.dead = False
		self.coordinates = None
	def move(self):
		pass
	def coords(self):
		return self.coordinates
class GridSquare(Sprite):
	def __init__(self, game, posx, posy):
		Sprite.__init__(self, game)
		self.gsq = self.game.canvas.create_rectangle(posx, posy, posx+50, posy+50, fill = '#aaaaaa')
		self.coordinates = Coords(posx, posy, posx+50, posy+50)
	def __contains__(self, point):
		if point.x <= self.coordinates.x2 and point.x >= self.coordinates.x1 and point.y <= self.coordinates.y2 and point.y >= self.coordinates.y1:
			return True
		return False
class Ship(Sprite):
	def __init__(self, game, size):
		Sprite.__init__(self, game)
		self.size = size
		if size == 1:
			self.img = PhotoImage(file='BattleShip1.gif')
			self.item = self.game.canvas.create_image(0, 450, image=self.img, anchor='nw')
		if size == 2:
			self.img = PhotoImage(file='BattleShip2.gif')
			self.item = self.game.canvas.create_image(0, 350, image=self.img, anchor='nw')
		self.evt2 = self.game.canvas.bind_all("<Button-1>", self.pick)
		self.evt4 = self.game.canvas.bind_all("<Button-2>", self.pick)
		self.coordinates = Coords(25, 450, 25+self.size*50, 450+self.size*50)
		self.picked = False
	def pick(self, evt):
		if Point(evt.x, evt.y) in self.coordinates:
			self.picked = True
		elif evt.x >= 50 and evt.x <= self.game.canvas_width and evt.y <= self.game.canvas_height and evt.y >= 0 and self.picked:
			self.game.canvas.delete(self.item)
			for i1 in self.game.grid:
				for i in i1:
					if Point(evt.x, evt.y) in i:
						self.item = self.game.canvas.create_image(i.coordinates.x1, i.coordinates.y1, image=self.img, anchor='nw')
			count = 0
			for x in ships:
				if x.size == self.size:
					count += 1
			if count == 0 and self.size == 1:
				ships.append(Ship(g, 1))
			if count in range(0, 2) and self.size == 2:
				ships.append(Ship(g, 1))
			self.picked = False
		else:
			self.picked = False
g = Game()
ships = []
ship = Ship(g, 1)
ship2 = Ship(g, 2)
ships.append(ship)
g.mainloop()
