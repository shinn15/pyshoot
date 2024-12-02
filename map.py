import pygame as pg

_ = False

#create map ==height width in seting.py
#num = objrennum
map_mini = [
	[1,1,1,1,1,1,1,1,1,1,1,1],
	[1,_,_,_,_,_,_,_,_,_,_,1],
	[1,_,2,2,2,2,_,2,2,2,_,1],
	[1,_,2,_,_,2,_,2,_,_,_,1],
	[1,_,_,_,_,_,_,2,_,_,_,1],
	[1,_,_,2,_,_,_,_,_,2,_,1],
	[1,1,1,1,1,1,1,1,1,1,1,1],
]

class map:
	def __init__(self,game):
		self.game = game
		self.map_mini=map_mini
		self.world_map={}
		self.get_map()

	def get_map(self):
		for j, row in enumerate(self.map_mini):
			for i, value in enumerate(row):
				if value:
					self.world_map[(i,j)] = value

	def draw(self):
		[pg.draw.rect(self.game.screen,'darkgray',(pos[0] * 100,pos[1] * 100,100,100),2)
		for pos in self.world_map]
