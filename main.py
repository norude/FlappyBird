#%%
import pygame
import flappyBird
import numpy as np
from os.path import join
import math
#%%
pygame.init()
pygame.font.init()
#%%
BIRD_SPRITES = [
pygame.transform.scale(pygame.image.load(join("images","bird1.png")),
				(flappyBird.BIRD_SCALE_X,
				 flappyBird.BIRD_SCALE_Y)
),
pygame.transform.scale(pygame.image.load(join("images","bird2.png")),
				(flappyBird.BIRD_SCALE_X,
				 flappyBird.BIRD_SCALE_Y)
),
pygame.transform.scale(pygame.image.load(join("images","bird3.png")),
				(flappyBird.BIRD_SCALE_X,
				 flappyBird.BIRD_SCALE_Y)
),
]

PIPE_TOP_SPRITE = pygame.image.load(join("images","pipe.png"))
PIPE_TOP_SPRITE = pygame.transform.scale(PIPE_TOP_SPRITE,
				(flappyBird.PIPE_SCALE_X,
				 PIPE_TOP_SPRITE.get_height())
)
PIPE_TOP_SPRITE = pygame.transform.flip(PIPE_TOP_SPRITE,True,False)
PIPE_BOTTOM_SPRITE = pygame.transform.flip(PIPE_TOP_SPRITE,False,True)
BG_SPRITE = pygame.image.load(join("images","bg.png"))
#%%
class Game:
	def __init__(self,surface:pygame.Surface):
		self.surface = surface
		self.HEIGHT = self.surface.get_height()
		self.WIDTH = self.surface.get_width()
		self.game = flappyBird.FlappyBird(self.HEIGHT,self.WIDTH)
		self.font = pygame.font.SysFont("", self.HEIGHT//20)
	def draw(self,key:bool,clock:pygame.time.Clock):
		self.surface.fill((255,255,255))
		self.game.compute_next(key)
		pipes,((birdY,birdAngle,temp),),score,dead,paralax = self.game.result
		for length,x in pipes:


			self.surface.blit(PIPE_BOTTOM_SPRITE,
				PIPE_BOTTOM_SPRITE.get_rect(
					bottomleft=(x,length,)
					)
			)
			self.surface.blit(PIPE_TOP_SPRITE,
				PIPE_TOP_SPRITE.get_rect(
					topleft=(x,length+flappyBird.PIPE_OFFSET_Y)
					)
			)

		bird_sprite = BIRD_SPRITES[paralax//20%3]
		bird_sprite = pygame.transform.rotate(bird_sprite,-birdAngle)

		rect = (bird_sprite.get_rect(center=(self.WIDTH//2,birdY+flappyBird.BIRD_SCALE_Y//2,))
		#.move(-pygame.math.Vector2(-flappyBird.BIRD_SCALE_X//2,0).rotate(birdAngle))
		)
		
		self.surface.blit(
			bird_sprite,
			rect
		)
		t1,t2 = temp
		pygame.draw.rect(self.surface,(255,0,0,),rect,5)
		pygame.draw.line(self.surface,(0,255,0,),(rect.left,t1),(rect.right,t1),5)
		pygame.draw.line(self.surface,(0,0,255,),(rect.left,t2),(rect.right,t2),5)

		text =self.font.render(f"{score}",True,(0,0,255))
		self.surface.blit(text,(self.WIDTH//2,self.HEIGHT//20))
		text =self.font.render(f"FPS:{clock.get_fps():.0f}",True,(0,0,255))
		self.surface.blit(text,(self.WIDTH//2,self.HEIGHT//20+36))
		return np.all(dead)
def main():
	screen = pygame.display.set_mode((500,700))
	game = Game(screen)
	running = True
	clock = pygame.time.Clock()
	while running:
		clock.tick(60)
		key = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type in (pygame.KEYDOWN,pygame.MOUSEBUTTONDOWN):
				key = True
		

		dead = Game.draw(game,key,clock)#game.draw()
		if dead and key:
			game = Game(screen)
		pygame.display.flip()

	return 0

if __name__ == "__main__":
	main()