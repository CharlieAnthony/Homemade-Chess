import pygame
from board import Board

class Chess_Game:

	def __init__(self):
		screen_width = 420
		screen_height = 420

		self.running = True

		pygame.display.init()

		self.screen = pygame.display.set_mode([screen_width, screen_height])

		colour = (48, 46, 43)

		self.screen.fill(colour)

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
					x_pixel, y_pixel = pygame.mouse.get_pos()
					x, y = board.get_clicked_cell((x_pixel, y_pixel))
					if board.selected_piece and (x, y) in board.available_moves.keys():
						board.move_piece(board.selected_piece, (x, y))
						if board.is_game_over():
							board.game_over = True
					else:
						board.get_available_moves((x, y))
					board.print_board()

			pygame.display.flip()

			self.clock.tick(60)