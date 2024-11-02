import pygame

class Chess_Game:

	def __init__(self):
		screen_width = 400
		screen_height = 400

		self.running = True

		pygame.display.init()

		self.screen = pygame.display.set_mode([screen_width, screen_height])

		window_title = "Chess"

		pygame.display.set_caption(window_title)

		pygame.display.flip()

		self.clock = pygame.time.Clock()

	def start_game(self):

		while self.running:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

			self.screen.fill((0, 0, 0))

			pygame.display.flip()

			self.clock.tick(60)