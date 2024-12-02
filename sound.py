import pygame as pg

class sound:
	def __init__(self,game):
		self.game=game
		pg.mixer.init()
		self.path = 'resource/sound/'
		self.weapon = pg.mixer.Sound(self.path+'shoot.wav')
		self.naides = pg.mixer.Sound(self.path+'naid.wav')
		self.neco = pg.mixer.Sound(self.path+'neco.mp3')
		self.moai = pg.mixer.Sound(self.path+'moai.mp3')
		self.player_hit = pg.mixer.Sound(self.path+'player_hit.wav')
		self.player_ded = pg.mixer.Sound(self.path+'player_ded.wav')
