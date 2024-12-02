from seting import *
import pygame as pg
import math

class player:
	def __init__(self,game):
		self.game=game
		self.x, self.y=PLAYER_POS
		self.angle=PLAYER_ANGLE
		self.shot=False
		self.health = PLAYER_MAX_HEALTH 
		self.rel=0

	def chck_gameover(self):
		if self.health < 1:
			self.game.object_render.gameover()
			pg.display.flip()
			pg.time.delay(1500)
			self.game.new_game()

#palyer if dmg
	def get_dmg(self,damage):
		self.health -=damage
		self.game.object_render.player_dmg()
		self.chck_gameover()

	def fire_gun(self,event):
		#shoot using space bar
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_SPACE and not self.shot and not self.game.weapon.reload:
				self.game.sound.weapon.play()
				self.shot=True
				self.game.weapon.reload=True


	#walking
	def movement(self):
		sin_a= math.sin(self.angle)
		cos_a= math.cos(self.angle)
		dx, dy = 0,0
		speed = PLAYER_SPEED * self.game.delta_time
		speed_sin = speed * sin_a
		speed_cos = speed * cos_a

		key = pg.key.get_pressed()
		if key[pg.K_w]:
			dx += speed_cos
			dy += speed_sin
		if key[pg.K_s]:
			dx += -speed_cos
			dy += -speed_sin
		if key[pg.K_a]:
			dx += speed_sin
			dy += -speed_cos
		if key[pg.K_d]:
			dx += -speed_sin
			dy += speed_cos

		self.wall_coll(dx,dy)

		#view
		if key[pg.K_LEFT]:
			self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
		if key[pg.K_RIGHT]:
			self.angle += PLAYER_ROT_SPEED * self.game.delta_time

		self.angle %= math.tau

	#check map position/colision
	def chck_wall(self,x,y):
		return (x,y) not in self.game.map.world_map
	#wall colision
	def wall_coll(self,dx,dy):
		player_scale = PLAYER_SIZE_SCALE/self.game.delta_time

		if self.chck_wall(int(self.x + dx *player_scale),int(self.y)):
			self.x += dx

		if self.chck_wall(int(self.x),int(self.y + dy *player_scale)):
			self.y += dy
#create plyer
	def draw(self):
		#debug for shoot view
		pg.draw.line(self.game.screen,'yellow',(self.x * 100,self.y * 100),
					(self.x * 100 + WIDTH * math.cos(self.angle),
					self.y * 100 + WIDTH * math.sin(self.angle)),2)

		pg.draw.circle(self.game.screen,'green', (self.x * 100,self.y * 100),15)
#view
	def mouse_control(self):
		mx,my= pg.mouse.get_pos()
		if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
			pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
		self.rel= pg.mouse.get_rel()[0]
		self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL,self.rel))
		self.angle +=self.rel *MOUSE_SENSITIVITY*self.game.delta_time


	def update(self):
		self.movement()
		self.mouse_control()

	@property
	def pos(self):
		return self.x, self.y

	@property
	def map_pos(self):
		return int(self.x), int(self.y)

	
