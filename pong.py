# Pong by Lorand

import pygame

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
		if player == 1:
			self.x = 20
		else:
			self.x = WIDTH - 20
		self.y = HEIGHT / 2
		self.rect.center = (self.x, self.y)




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
				player1 = Paddle(1)
				sprites_all.add(player1)
				player2 = Paddle(2)
				sprites_all.add(player2)
				
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