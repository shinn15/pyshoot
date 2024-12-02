import pygame as pg
from seting import *

#draw object in game
class object_render:
	def __init__(self,game):
		self.game = game
		self.screen = game.screen
		self.wall_texture = self.load_wall_img()
		self.sky_img= self.get_resource('resource/wall/sk2.jpg',(WIDTH,HALF_HEIGHT))
		self.sky_offset=0

		self.blod_scren = self.get_resource('resource/sprites/blood_screen.png',RES)
		self.digit_size=90
		self.digit_img=[self.get_resource(f'resource/sprites/digits/{i}.png',[self.digit_size] * 2)
						for i in range(11)]
		self.digits= dict(zip(map(str, range(11)),self.digit_img))

		self.gameover_img= self.get_resource('resource/sprites/game_over.png',RES)
		self.win_img= self.get_resource('resource/sprites/win.png',RES)

	def draw(self):
		self.draw_background()
		self.render_game_object()
		self.draw_healthbar()

	def gameover(self):
		self.screen.blit(self.gameover_img,(0,0))

	def win(self):
		self.screen.blit(self.win_img,(0,0))

	def draw_healthbar(self):
		health=str(self.game.player.health)
		for i, char in enumerate(health):
			self.screen.blit(self.digits[char],(i*self.digit_size,0))
		self.screen.blit(self.digits['10'],((i+1)*self.digit_size,0))

	def player_dmg(self):
		self.screen.blit(self.blod_scren,(0,0))
		self.game.sound.player_hit.play()

	def draw_background(self):
		#sky follow viewpov
		self.sky_offset = (self.sky_offset+4.0*self.game.player.rel)%WIDTH
		self.screen.blit(self.sky_img,(-self.sky_offset,0))
		self.screen.blit(self.sky_img,(-self.sky_offset+WIDTH,0))
		#floor
		pg.draw.rect(self.screen,FLOOR_COLOR,(0,HALF_HEIGHT,WIDTH,HEIGHT))

	def render_game_object(self):
		list_object = sorted(self.game.raycasing.object_to_render, key=lambda t: t[0], reverse=True)
		for depth, image, pos in list_object:
			self.screen.blit(image,pos)

	@staticmethod
	def get_resource(path,res=(RSC_SIZE,RSC_SIZE)):
		img=pg.image.load(path).convert_alpha()
		return pg.transform.scale(img,res)
#map wall
	def load_wall_img(self):
		return{
			1: self.get_resource('resource/wall/wall1.png'),
			2: self.get_resource('resource/wall/wall2.png'),
			3: self.get_resource('resource/wall/n3.png'),
			4: self.get_resource('resource/wall/n4.png'),
		}
