# Pong by Lorand

import pygame
import random

WIDTH = 800
HEIGHT = 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

pygame.mixer.init()

pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)

class Paddle(pygame.sprite.Sprite):
	def __init__(self, player):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((15, 100))
		self.image.fill("white")
		self.rect = self.image.get_rect()
		self.player = player
		if self.player == 1:
			self.x = 20
		else:
			self.x = WIDTH - 20
		self.y = HEIGHT / 2
		self.rect.center = (self.x, self.y)

	def update(self):
		if self.player == 1:
			self.rect.y += joystick.get_axis(1) * 10
		else:
			self.rect.y += joystick.get_axis(3) * 10
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT
		if self.rect.top < 0:
			self.rect.top = 0

class Ball(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((15, 15))
		self.image.fill("white")
		self.rect = self.image.get_rect()
		self.x = WIDTH / 2
		self.y = HEIGHT / 2
		self.rect.center = (self.x, self.y)
		self.vx = random.uniform(6, 10) * random.choice([-1, 1])
		self.vy = random.uniform(-4, 4)

	def update(self):
		self.rect.x += self.vx
		self.rect.y += self.vy

def draw_text(surf, text, size, x, y, align):
	font_name = pygame.font.match_font("Comic Sans MS")
	font = pygame.font.Font(font_name, size)
	text_surf = font.render(text, True, "white")
	text_rect = text_surf.get_rect()
	if align == "center":
		text_rect.center = (x, y)
	elif align == "topright":
		text_rect.topright = (x, y)
	else:
		text_rect.topleft = (x, y)
	surf.blit(text_surf, text_rect)

score = (0, 0)
main_menu = True
running = True

while running:
	if main_menu:
		screen.fill("black")
		draw_text(screen, "Pong", 50, WIDTH / 2, HEIGHT * 0.2, "center")
		draw_text(screen, f"Last score: {score[0]} - {score[1]}", 20, WIDTH / 2, HEIGHT * 0.35, "center")
		draw_text(screen, "Controls (Xbox):", 20, WIDTH / 2, HEIGHT * 0.44, "center")
		draw_text(screen, "B to start game", 20, WIDTH / 2, HEIGHT * 0.5, "center")
		draw_text(screen, "X to exit game", 20, WIDTH / 2, HEIGHT * 0.55, "center")
		draw_text(screen, "LS (up and down) to move player 1", 20, WIDTH / 2, HEIGHT * 0.62, "center")
		draw_text(screen, "RS (up and down) to move player 2", 20, WIDTH / 2, HEIGHT * 0.67, "center")
		pygame.display.flip()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.JOYBUTTONDOWN and event.button == 2):
				running = False
			if event.type == pygame.JOYBUTTONDOWN and event.button == 1:
				main_menu = False
				
				sprites_all = pygame.sprite.Group()
				paddle1 = Paddle(1)
				sprites_all.add(paddle1)
				paddle2 = Paddle(2)
				sprites_all.add(paddle2)
				ball = Ball()
				sprites_all.add(ball)
				
				score = (0, 0)

		clock.tick(FPS)

	else:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		sprites_all.update()
				
		if score[0] >= 10 or score[1] >= 10:
			main_menu = True
				

		
		screen.fill("black")
		sprites_all.draw(screen)
		draw_text(screen, f"{score[0]} - {score[1]}", 25, WIDTH / 2, 20, "center")
		pygame.display.flip()

		clock.tick(FPS)

pygame.quit()