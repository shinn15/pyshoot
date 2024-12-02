import pygame as pg
import sys
from seting import *
from map import *
from player import *
from raycasing import *
from object_render import *
from sprite_obj import *
from object_handler import *
from weapon import *
from sound import *
from bot_pathfind import *



#game run
class Run_game:
	def __init__(self):
		pg.init()
		#mouse arrow visibiblity
		pg.mouse.set_visible(False)

		self.screen = pg.display.set_mode(RES)
		self.clock = pg.time.Clock()
		self.delta_time = 1
		
		#animation
		self.global_triger = False
		self.global_event= pg.USEREVENT + 0
		pg.time.set_timer(self.global_event,40)





		self.new_game()


	def new_game(self):
		self.map=map(self)
		self.player=player(self)
		self.object_render = object_render(self)
		self.raycasing=raycasing(self)
		self.object_handler=object_handler(self)
		self.weapon=weapon_pl(self)
		self.sound=sound(self)
		self.bot_pathfind=bot_pathfind(self)
	

	def update(self):
		self.player.update()
		self.raycasing.update()
		self.object_handler.update()

		self.weapon.update()
		pg.display.flip()
		self.delta_time = self.clock.tick(FPS)
		pg.display.set_caption(f'{self.clock.get_fps() :.1f}')


	def draw(self):
		self.object_render.draw()
		self.weapon.draw()
		#2d
		#self.screen.fill('black')
		#self.map.draw()
		#self.player.draw()


	def chck_event(self):
		self.global_triger = False
		for event in pg.event.get():
			#exit game
			if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
				pg.quit()
				sys.exit()
			elif event.type == self.global_event:
				self.global_triger=True

			self.player.fire_gun(event)


	def run(self):
		while True:
			self.chck_event()
			self.update()
			self.draw()




if __name__ == '__main__':
	game= Run_game()
	game.run()