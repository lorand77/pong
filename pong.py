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
sound_wall = pygame.mixer.Sound("assets/pongblip_e5.wav")
sound_mid_paddle = pygame.mixer.Sound("assets/pongblip_d5.wav")
sound_edge_paddle = pygame.mixer.Sound("assets/pongblip_f5.wav")

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
			self.rect.y += joystick.get_axis(1) * 12
		else:
			self.rect.y += joystick.get_axis(3) * 12
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
		self.vx = random.uniform(7, 10) * random.choice([-1, 1])
		self.vy = random.uniform(-4, 4)
		self.active = True

	def move(self):
		self.x += self.vx
		self.y += self.vy
		if self.y < 0:
			self.y = -self.y
			self.vy = -self.vy
			sound_wall.play()
		if self.y > HEIGHT:
			self.y = 2 * HEIGHT - self.y
			self.vy = -self.vy
			sound_wall.play()
		self.rect.center = (self.x, self.y)

	def has_reached_endline(self):
		if self.rect.right < 0 and self.active == True:
			score[1] += 1
			self.active = False
			self.last_active_time = pygame.time.get_ticks()
		if self.rect.left > WIDTH and self.active == True:
			score[0] += 1
			self.active = False
			self.last_active_time = pygame.time.get_ticks()

	def reactivate(self):
		now = pygame.time.get_ticks()
		if self.active == False and now - self.last_active_time > 1000:
			self.active = True
			self.x = WIDTH / 2
			self.y = HEIGHT / 2
			self.rect.center = (self.x, self.y)
			self.vx = random.uniform(7, 10) * random.choice([-1, 1])
			self.vy = random.uniform(-4, 4)

	def touches_paddle(self):
		hits = pygame.sprite.spritecollide(ball, sprites_paddles, dokill = False)
		if hits:
			self.vx = -self.vx
			if hits[0].player == 1:
				self.x = 29
			else:
				self.x = WIDTH - 29
			self.rect.centerx = self.x
			if hits[0].y - self.y > 30:
				self.vy -= random.uniform(4, 6)
			if self.y - hits[0].y > 30:
				self.vy += random.uniform(4, 6)
			if abs(hits[0].y - self.y) > 30:
				sound_edge_paddle.play()
			else:
				sound_mid_paddle.play()

	def update(self):
		self.move()
		self.has_reached_endline()
		self.touches_paddle()
		self.reactivate()

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

score = [0, 0]
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
				sprites_paddles = pygame.sprite.Group()
				paddle1 = Paddle(1)
				sprites_all.add(paddle1)
				sprites_paddles.add(paddle1)
				paddle2 = Paddle(2)
				sprites_all.add(paddle2)
				sprites_paddles.add(paddle2)
				ball = Ball()
				sprites_all.add(ball)
				
				score = [0, 0]

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
		draw_text(screen, f"{score[0]} - {score[1]}", 55, WIDTH / 2, 35, "center")
		pygame.display.flip()

		clock.tick(FPS)

pygame.quit()