import pygame.draw


class Board:
	def __init__(self, screen):
		self.state = [["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
						["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
						["", "", "", "", "", "", "", ""],
						["", "", "", "", "", "", "", ""],
						["", "", "", "", "", "", "", ""],
						["", "", "", "", "", "", "", ""],
						["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
						["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]
		self.available_moves = [(3, 4), (4, 4), (3, 3), (4, 3)]
		self.square_size = 40
		self.screen = screen
		self.x_offset, self.y_offset = 30, 30
		self.is_white_turn = True
		self.can_white_castle = True
		self.can_black_castle = True
		self.selected_piece = None

		self.print_board()

	def print_board(self):

		WHITE, GREEN = (235, 236, 208), (115, 149, 82)

		for y, row in enumerate(self.state):
			for x, val in enumerate(row):
				colour_calc = x + (0 if y % 2 == 0 else 1)
				colour = WHITE if colour_calc % 2 == 0 else GREEN
				x_pos, y_pos = self.x_offset + (x * self.square_size), self.y_offset + (y * self.square_size)
				rect = pygame.Rect(x_pos, y_pos, self.square_size, self.square_size)
				pygame.draw.rect(self.screen, colour, rect)
				if val:
					img = pygame.image.load(f"./assets/{val}.png")
					img_resized = pygame.transform.scale(img, (self.square_size, self.square_size))
					self.screen.blit(img_resized, (x_pos, y_pos))

		if self.selected_piece:
			for (x, y) in self.available_moves:
				x_pos, y_pos = self.x_offset + (x * self.square_size), self.y_offset + (y * self.square_size)
				img = pygame.image.load("./assets/hint.png")
				img_resized = pygame.transform.scale(img, (self.square_size, self.square_size))
				self.screen.blit(img_resized, (x_pos, y_pos))

		pygame.display.flip()

	def get_clicked_cell(self, pos):
		x_pos, y_pos = pos
		x = (x_pos - self.x_offset) // self.square_size
		y = (y_pos - self.y_offset) // self.square_size
		return x, y

	def get_available_moves(self, pos):
		x, y = pos
		piece = self.state[y][x]
		if not piece:
			self.selected_piece = None
			return []
		self.selected_piece = (x, y)
		available_moves = []
		if piece == "wp":
			if not self.state[y-1][x]:
				available_moves.append((x, y-1))
				if y == 6 and not self.state[y-2][x]:
					available_moves.append((x, y-2))

		self.available_moves = available_moves
		self.print_board()
		return available_moves

	def move_piece(self, new_pos):
		x_old, y_old = self.selected_piece
		x_new, y_new = new_pos
		piece = self.state[y_old][x_old]
		if (self.is_white_turn and piece[0] != 'w') or (not self.is_white_turn and piece[0] != 'b'):
			print("not your turn!")
			self.selected_piece = ""
			return
		self.state[y_old][x_old] = ""
		self.state[y_new][x_new] = piece
		self.available_moves = []
		self.print_board()
		self.selected_piece = ""
		self.is_white_turn = not self.is_white_turn

	def is_check(self, is_white=True):
		return False