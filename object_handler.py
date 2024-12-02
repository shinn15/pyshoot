from sprite_obj import *
from bot import *

class object_handler:
	def __init__(self,game):
		self.game = game
		self.sprite_list=[]
		self.bot_list=[]
		self.bot_path_sp='resource/bot'
		#object
		self.static_sprite='resource/sprites/staticimg1.png'
		self.anim_sprite='resource/sprites/nai_sprite/'

		#bot
		add_sprite = self.add_sprite
		add_bot = self.add_bot
		self.bot_pos={}

		# add object animation to map
		#add_sprite(sprite_obj(game))
		#add_sprite(animated_sprites(game))
		#add_sprite(animated_sprites(game, pos=(1.5,1.5)))
		#add_sprite(animated_sprites(game, pos=(1.5,7.5)))

		#add_sprite(animated_sprites(game,path=self.anim_sprite + 'nainai1.png',
		 #pos=(14.5,7.5)))

		#add bot in map
		add_bot(bot_npc(game))
		add_bot(bot_npc(game,pos=(7.5,5.5)))

		add_bot(nai_bot(game))

	def update(self):
		self.bot_pos = {bot.map_pos for bot in self.bot_list if bot.alive}
		[sprite.update() for sprite in self.sprite_list]
		[bot.update() for bot in self.bot_list]
		self.chck_win()

#check if no bot and win
	def chck_win(self):
		if not len(self.bot_pos):
			self.game.object_render.win()
			pg.display.flip()
			pg.time.delay(1500)
			self.game.new_game()
	        

	def add_bot(self,bot):
		self.bot_list.append(bot)

	def add_sprite(self,sprite):
		self.sprite_list.append(sprite)
