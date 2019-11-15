# principles of computing
# Week 1: project
# Game 2048: merge function (100%)


def merge(line):
	"""
	Performs the tile merging of the 2048 game.
	Input is a list representing a game line.
	Output is a new list reflecting merges.
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


print(merge([0, 4, 2, 0, 2]))
