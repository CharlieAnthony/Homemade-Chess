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
		self.available_moves = {}
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
			for (x, y) in self.available_moves.keys():
				x_pos, y_pos = self.x_offset + (x * self.square_size), self.y_offset + (y * self.square_size)
				img = pygame.image.load("./assets/hint_danger.png" if self.available_moves[(x, y)] else "./assets/hint.png")
				img_resized = pygame.transform.scale(img, (self.square_size, self.square_size))
				self.screen.blit(img_resized, (x_pos, y_pos))

		pygame.display.flip()

	def get_clicked_cell(self, pos):
		x_pos, y_pos = pos
		x = (x_pos - self.x_offset) // self.square_size
		y = (y_pos - self.y_offset) // self.square_size
		return x, y

	def get_raw_moves(self, pos):
		x, y = pos
		piece = self.state[y][x]
		raw_moves = []
		if not piece:
			return []
		# pawn moves
		if piece[1] == "p":
			direction = 1 if piece[0] == "b" else -1
			if not self.is_valid((x, y + direction)):
				return []
			if self.is_empty((x, y + direction)):
				raw_moves.append((x, y + direction))
				if (y == 6 and piece[0] == "w") or (y == 1 and piece[0] == "b"):
					if self.is_empty((x, y + (2 * direction))):
						raw_moves.append((x, y + (2 * direction)))
			for x_dir in [-1, 1]:
				capture_pos = (x + x_dir, y + direction)
				if self.is_valid(capture_pos) and not self.is_empty(capture_pos) and self.is_opposition_piece(capture_pos, piece[0]):
					raw_moves.append(capture_pos)
		# king moves
		if piece[1] == "k":
			king_moves = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
			for move_x, move_y in king_moves:
				new_pos = (x + move_x, y + move_y)
				if self.is_valid(new_pos) and not self.is_opposition_piece(new_pos, piece[0]):
					raw_moves.append(new_pos)
		# knight moves
		if piece[1] == "n":
			knight_moves = [(2, 1), (2, -1), (1, 2), (1, -2), (-2, 1), (-2, -1), (-1, 2), (-1, -2)]
			for move_x, move_y in knight_moves:
				new_pos = (x + move_x, y + move_y)
				if self.is_valid(new_pos) and not self.is_opposition_piece(new_pos, piece[0]):
					raw_moves.append(new_pos)
		# bishop/queen moves
		# TODO: repeat code. Could be more concise
		if piece[1] == "b" or piece[1] == "q":
			dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
			for d_x, d_y in dirs:
				new_pos = (x, y)
				while True:
					old_x, old_y = new_pos
					new_pos = (old_x + d_x, old_y + d_y)
					if self.is_valid(new_pos):
						if self.is_empty(new_pos):
							raw_moves.append(new_pos)
						else:
							if self.is_opposition_piece(new_pos, piece[0]):
								raw_moves.append(new_pos)
							break
					else:
						break
		# rook/queen moves
		if piece[1] == "r" or piece[1] == "q":
			dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
			for d_x, d_y in dirs:
				new_pos = (x, y)
				while True:
					old_x, old_y = new_pos
					new_pos = (old_x + d_x, old_y + d_y)
					if self.is_valid(new_pos):
						if self.is_empty(new_pos):
							raw_moves.append(new_pos)
						else:
							if self.is_opposition_piece(new_pos, piece[0]):
								raw_moves.append(new_pos)
							break
					else:
						break
		return raw_moves

	def get_available_moves(self, pos):
		# TODO: makes a state, passes to is_check() method, if no then adds to available_moves
		x, y = pos
		piece = self.state[y][x]
		if not piece or (piece and (piece[0] == "w") != self.is_white_turn):
			self.selected_piece = None
			return {}
		self.selected_piece = (x, y)
		available_moves = {}
# -=-=-=-=-=- WHITE PIECES -=-=-=-=-=-
		if piece == "wp":
			if y > 0 and not self.state[y-1][x]:
				available_moves[(x, y-1)] = False
				if y == 6 and not self.state[y-2][x]:
					available_moves[(x, y-2)] = False
			if y > 0:
				if x > 0 and self.state[y-1][x-1] and self.state[y-1][x-1][0] == "b":
					available_moves[(x-1, y-1)] = True
				if x < 7 and self.state[y-1][x+1] and self.state[y-1][x+1][0] == "b":
					available_moves[(x+1, y-1)] = True
# -=-=-=-=-=- BLACK PIECES -=-=-=-=-=-
		if piece == "bp":
			if y < 7 and not self.state[y+1][x]:
				available_moves[(x, y+1)] = False
				if y == 1 and not self.state[y+2][x]:
					available_moves[(x, y+2)] = False
			if y < 7:
				if x > 0 and self.state[y+1][x-1] and self.state[y+1][x-1][0] == "w":
					available_moves[(x-1, y+1)] = True
				if x < 7 and self.state[y+1][x+1] and self.state[y+1][x+1][0] == "w":
					available_moves[(x+1, y+1)] = True
		if piece[-1] == "k":
			king_moves = [(1, 1), (0, 1), (-1, 1), (1, 0), (-1, 0), (1, -1), (0, -1), (-1, -1)]
			for move in king_moves:
				new_x, new_y = x + move[0], y + move[1]
				if 0 <= new_x <= 7 and 0 <= new_y <= 7:
					new_state = self.get_new_state((x, y), (new_x, new_y))
					if self.state[new_y][new_x] == "" and not self.is_check(new_state, self.is_white_turn):
						available_moves[(new_x, new_y)] = False

		self.available_moves = available_moves
		return available_moves

	def move_piece(self, old_pos, new_pos):
		if new_pos not in self.available_moves:
			return
		self.state = self.get_new_state(old_pos, new_pos)

		self.is_white_turn = not self.is_white_turn
		print("is check?")
		self.is_check(self.state, self.is_white_turn)
		self.available_moves = {}
		self.selected_piece = None

	def get_new_state(self, old_pos, new_pos):
		state = [[x for x in row] for row in self.state]
		x_old, y_old = old_pos
		x_new, y_new = new_pos
		piece = state[y_old][x_old]
		state[y_old][x_old] = ""
		state[y_new][x_new] = piece
		return state

	def is_check(self, state, is_white):
		"""
		Checks if player is in check
		:param state: state of board
		:param is_white: if white is in check
		:return: Boolean
		"""
		colour = "w" if is_white else "b"
		opp_king_pos = self.find_king_position(state, is_white)
		for y, row in enumerate(state):
			for x, piece in enumerate(row):
				if not self.is_empty((x, y)) and self.is_opposition_piece((x, y), colour):
					moves = self.get_raw_moves((x, y))
					if opp_king_pos in moves:
						print("yes\n\n")
						return True
		print("no\n\n")
		return False

	def find_king_position(self, state, is_white):
		"""
		Finds the position of the king
		:param state: board state
		:param is_white: if looking for white king or not
		:return: (x, y) pos on board of king
		"""
		piece = "wk" if is_white else "bk"
		for y, row in enumerate(state):
			for x, p in enumerate(row):
				if p == piece:
					return x, y
		return None

	def is_valid(self, pos):
		x, y = pos
		return 0 <= x <= 7 and 0 <= y <= 7

	def is_empty(self, pos):
		x, y = pos
		return self.state[y][x] == ""

	def is_opposition_piece(self, pos, colour):
		if self.is_empty(pos):
			return False
		x, y = pos
		return self.state[y][x][0] != colour