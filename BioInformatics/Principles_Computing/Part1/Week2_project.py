# principles of computing
# Week 2: project
# Game 2048: FULL

"""
Clone of 2048 game.
"""

#import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
	"""
	Helper function that merges a single row or column in 2048
	"""
	result = line[:]
	line_index = 1
	# cell represents the current tile we are aiming to set correct
	# line_index is a different cell further down the line
	for cell in range(len(line) - 1):
		while line_index < len(line):
			if result[line_index] == 0:
				line_index += 1
			# in case current cell is 0, merge with non-zero cell
			# but do not break out of while loop as this merge does not count
			elif result[cell] == 0:
				result[cell] += result[line_index]
				result[line_index] = 0
				line_index += 1
			elif result[line_index] == result[cell]:
				result[cell] += result[line_index]
				result[line_index] = 0
				line_index = cell + 2
				break
			elif result[line_index] != result[cell]:
				line_index = cell + 2
				break
	return result

class TwentyFortyEight:
	"""
	Class to run the game logic.
	"""

	def __init__(self, grid_height, grid_width):
		self.grid_height = grid_height
		self.grid_width = grid_width

		# pre-compute first tiles for each direction (help with move, later)
		self.first_tiles = {'UP': [], 'DOWN': [], 'LEFT': [], 'RIGHT': []}
		for row in range(self.grid_height):
			for col in range(self.grid_width):
				if row == 0:
					self.first_tiles['UP'].append((row, col))
				if row == self.grid_height - 1:
					self.first_tiles['DOWN'].append((row, col))
				if col == 0:
					self.first_tiles['LEFT'].append((row, col))
				if col == self.grid_width - 1:
					self.first_tiles['RIGHT'].append((row, col))
		self.reset()

	def reset(self):
		"""
		Reset the game so the grid is empty except for two
		initial tiles.
		"""
		self.grid = [[0 for i in range(self.grid_width)] \
					 for column in range(self.grid_height)]
		self.new_tile()
		self.new_tile()

	def __str__(self):
		"""
		Return a string representation of the grid for debugging.
		"""
		result = ''
		for row in self.grid:
			result += str(row) + '\n'
		return result

	def get_grid_height(self):
		"""
		Get the height of the board.
		"""
		return self.grid_height

	def get_grid_width(self):
		"""
		Get the width of the board.
		"""
		return self.grid_width

	def move(self, direction):
		"""
		Move all tiles in the given direction and add
		a new tile if any tiles moved.
		"""
		# replace with your code
		pass

	def new_tile(self):
		"""
		Create a new tile in a randomly selected empty square.
		The tile should be 2 90% of the time and 4 10% of the time.
		"""
		# find empty squares
		empty_squares = []
		for row in range(len(self.grid)):
			for col in range(len(self.grid[0])):
				if self.grid[row][col] == 0:
					empty_squares.append((row,col))
		# catch game over (no more empty squares)
		if len(empty_squares) == 0:
			return

		new_tile_pos = random.choice(empty_squares)
		new_tile = random.choices([2, 4], weights=[.9, .1])
		self.grid[new_tile_pos[0]][new_tile_pos[1]] = new_tile[0]

	def set_tile(self, row, col, value):
		"""
		Set the tile at position row, col to have the given value.
		"""
		self.grid[row][col] = value

	def get_tile(self, row, col):
		"""
		Return the value of the tile at position row, col.
		"""
		return self.grid[row][col]


#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))


a = TwentyFortyEight(4, 5)
print(a)

