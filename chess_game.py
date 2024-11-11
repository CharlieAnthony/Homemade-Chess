import pygame
from board import Board

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

		board = Board(self.screen)

		while self.running:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				elif event.type == pygame.MOUSEBUTTONDOWN:
					x, y = pygame.mouse.get_pos()
					x, y = board.get_clicked_cell((x, y))
					if board.selected_piece:
						board.move_piece((x, y))
					else:
						board.get_available_moves((x, y))
					board.print_board()

			pygame.display.flip()

			self.clock.tick(60)