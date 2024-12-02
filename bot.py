from sprite_obj import *
from random import *
from sound import *


class bot_npc(animated_sprites):
	def __init__(self,game,path='resource/bot/neco_bot/0.png',pos=(6.5,4.5),
		scale=0.6,shift=0.38,animation_time=180):
		super().__init__(game,path,pos,scale,shift,animation_time)
		self.attck_anim=self.get_images(self.path + '/attk')
		self.death_anim=self.get_images(self.path + '/death')
		self.idle_anim=self.get_images(self.path + '/idle')
		self.pain_anim=self.get_images(self.path + '/pain')
		self.walk_anim=self.get_images(self.path + '/walk')

		self.sound=sound(self)
		self.sound=self.sound.neco.play()

		self.attk_dist=randint(1,2)
		self.speed=0.03
		self.size=10
		self.health=100
		self.attk_dmg=10
		self.accuracy=0.15
		self.alive=True
		self.pain=False
		self.frame_counter=0

		self.ray_cast_value = False
		self.bot_search_trigger=False

	def update(self):
		self.check_animation_time()
		self.get_sprite()
		self.logic_run()

		#debug bot view
		#self.draw_raycast()



#bot animation
	def animate_ded(self):
		if not self.alive:
			if self.game.global_triger and self.frame_counter < len(self.death_anim) - 1:
				self.death_anim.rotate(-1)
				self.image = self.death_anim[0]
				self.frame_counter += 1

	def animate_hit(self):
		self.animate(self.pain_anim)
		if self.animation_trigger:
			self.pain = False

	def chck_hit_in_bot(self):
		if self.ray_cast_value and self.game.player.shot:
			if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
				self.sound=self.sound
				self.game.player.shot = False
				self.pain = True


				self.health -= self.game.weapon.damage
				self.chck_health()

#bot logic
	def bot_chck_wall(self,x,y):
		return (x,y) not in self.game.map.world_map
	#bot wall colision
	def bot_wall_coll(self,dx,dy):
		if self.bot_chck_wall(int(self.x + dx * self.size),int(self.y)):
			self.x += dx

		if self.bot_chck_wall(int(self.x),int(self.y + dy * self.size)):
			self.y += dy

	def bot_move(self):
		next_pos = self.game.bot_pathfind.get_path(self.map_pos,self.game.player.map_pos)
		next_x,next_y = next_pos

		#debug bot move
		#pg.draw.rect(self.game.screen,'blue',(100 *next_x,100*next_y,100,100))

		#bot move and not same pos
		if next_pos not in self.game.object_handler.bot_pos:
			angle=math.atan2(next_y + 0.5 - self.y,next_x + 0.5 - self.x)
			dx=math.cos(angle)*self.speed
			dy=math.sin(angle)*self.speed
			self.bot_wall_coll(dx,dy)
	
	def bot_attk(self):
		if self.animation_trigger:
			self.sound=self.sound

			if random() < self.accuracy:
				self.game.player.get_dmg(self.attk_dmg)

	def chck_health(self):
		if self.health < 1:
			self.alive = False
			self.sound=self.sound
#run logic
	def logic_run(self):
		if self.alive:
			self.ray_cast_value = self.ray_cast_player_npc()

			#if bot is hit
			self.chck_hit_in_bot()
			if self.pain:
				self.animate_hit()
			#if bot see player
			elif self.ray_cast_value:
				self.bot_search_trigger=True
				#bot attka ot walk
				if self.dist < self.attk_dist:
					self.animate(self.attck_anim)
					self.bot_attk()
				else:
					self.animate(self.walk_anim)
					self.bot_move()

			elif self.bot_search_trigger:
				self.animate(self.walk_anim)
				self.bot_move()

			else:
				self.animate(self.idle_anim)
		else:
			self.animate_ded()


	@property
	def map_pos(self):
		return int(self.x), int(self.y)

	def ray_cast_player_npc(self):
		if self.game.player.map_pos == self.map_pos:
			return True
		wall_dist_v, wall_dist_h=0,0
		player_dist_v, player_dist_h=0,0
		#player pos
		ox, oy = self.game.player.pos
		x_map, y_map = self.game.player.map_pos

		ray_angle= self.theta

		sin_a=math.sin(ray_angle)
		cos_a=math.cos(ray_angle)

			#horizobtal
		y_hor,dy = (y_map +1,1) if sin_a > 0 else (y_map - 1e-6,-1)

		depth_hor = (y_hor - oy)/sin_a
		x_hor = ox+depth_hor *cos_a

		delta_depth = dy/sin_a
		dx = delta_depth*cos_a
			#horizontal view
		for i in range(MAX_DEPTH):
			tile_hor = int(x_hor),int(y_hor)
			if tile_hor == self.map_pos:
				player_dist_h = depth_hor
				break

			if tile_hor in self.game.map.world_map:
				wall_dist_h=depth_hor
				break
				x_hor += dx
				y_hor += dy
				depth_hor += delta_depth

			#vertical
		x_vert, dx = (x_map +1,1) if cos_a > 0 else (x_map - 1e-6,-1)

		depth_vert = (x_vert - ox)/cos_a
		y_vert = oy+depth_vert *sin_a

		delta_depth = dx/cos_a
		dy = delta_depth*sin_a
			#vertical view
		for i in range(MAX_DEPTH):
			tile_vert = int(x_vert),int(y_vert)
			if tile_vert ==self.map_pos:
				player_dist_v = depth_vert
				break

			if tile_vert in self.game.map.world_map:
				wall_dist_v = depth_hor
				break
			x_vert += dx
			y_vert += dy
			depth_vert += delta_depth

		player_dist = max(player_dist_v,player_dist_h)
		wall_dist = max(wall_dist_v,wall_dist_h)

		if 0 < player_dist < wall_dist or not wall_dist:
			return True
		return False
#debug
	def draw_raycast(self):
		pg.draw.circle(self.game.screen,'red',(100*self.x,100 *self.y),15)
		if self.ray_cast_player_npc():
			pg.draw.line(self.game.screen,'green',(100*self.game.player.x,100*self.game.player.y),
						(100*self.x,100*self.y),2)


#add bot
class neco_bot(bot_npc):
	def __init__(self,game,path='resource/bot/neco_bot/0.png',pos=(5.5,3.5),
		scale=0.6,shift=0.38,animation_time=180):

		super().__init__(game,path,pos,scale,shift,animation_time)



class nai_bot(bot_npc):
	def __init__(self,game,path='resource/bot/nai_bot/0.png',pos=(6.5,3.5),
		scale=0.7,shift=0.35,animation_time=180):
		super().__init__(game,path,pos,scale,shift,animation_time)
		#for music
		self.sound=sound(self)
		self.sound=self.sound.naides.play()

		self.attk_dist=randint(1,2)
		self.speed=0.04
		self.size=10
		self.health=100
		self.attk_dmg=5
		self.accuracy=0.15
		self.alive=True
		self.pain=False
		self.frame_counter=0

