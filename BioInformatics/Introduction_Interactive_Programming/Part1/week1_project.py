# week 1 project
# Rock - Paper - Scissors - Lizard - Spock

import sys
import random

if len(sys.argv) != 2:
	print('''Usage: provide this program with one command line argument:
			argv1: users choice of weapon: rock, paper, scissors,
			lizard, Spock''')
	sys.exit()


def name_to_number(name):
	"converts weapon selection to number for easier comparison"
	if name == 'rock': return 0
	elif name == 'Spock': return 1
	elif name == 'paper': return 2
	elif name == 'lizard': return 3
	elif name == 'scissors': return 4
	else:
		print('Error: please provide an valid choice.')
		return "ERROR"

def number_to_name(number):
	"converts computer's weapon selection to human readable text"
	if number == 0: return 'rock'
	elif number == 1: return 'Spock'
	elif number == 2: return 'paper'
	elif number == 3: return 'lizard'
	elif number == 4: return 'scissors'

def rpsls(player_choice):
	"prints to terminal the player's choice and begins internal processing"
	player_weapon = name_to_number(player_choice)
	if player_weapon == "ERROR":	return
	computer_weapon = random.randrange(0, 5)

	print('Player chooses ' + player_choice)
	print('Computer chooses ' + number_to_name(computer_weapon))

	if player_weapon - computer_weapon == 0:
		print('The game ended in a tie.', end='\n\n')
	elif (player_weapon - computer_weapon) % 5 <= 2:
		print('The player has won!!!', end='\n\n')
	else:
		print('The Computer has won :(', end='\n\n')

	return


if __name__ == '__main__':
	rpsls(sys.argv[1])
