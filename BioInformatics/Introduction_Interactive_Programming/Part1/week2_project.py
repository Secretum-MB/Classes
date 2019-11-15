# week 2 project

# Guess my number

# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random

range_max = 100

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number, num_guesses
    secret_number = random.randrange(0, range_max)

    if range_max == 100:
        num_guesses = 7
    else:
        num_guesses = 10

    print("Guess the number between 0 and %s" % str(range_max - 1))
    print("You have %s guesses remaining" % num_guesses)


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game
    global range_max
    range_max = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game
    global range_max
    range_max = 1000
    new_game()

def input_guess(guess):
    # main game logic goes here
    global num_guesses
    print("Guess was " + str(int(guess)))
    if secret_number - int(guess) > 0:
        num_guesses -= 1
        print("Higher!")
        print("You have %s guesses remaining" % num_guesses)

        if num_guesses == 0:
            print("Sorry, you lose.")
            print
            new_game()

    elif secret_number - int(guess) < 0:
        num_guesses -= 1
        print("Lower!")
        print("You have %s guesses remaining" % num_guesses)

        if num_guesses == 0:
            print("Sorry, you lose.")
            print
            new_game()
    else:
        print("Correct!")
        new_game()


# create frame
frame = simplegui.create_frame("Guess my Number", 200, 200)
frame.add_input("Enter guess", input_guess, 100)

frame.add_button("Range is [0, 100)", range100, 150)
frame.add_button("Range is [0, 1000)", range1000, 150)


# register event handlers for control elements and start frame


# call new_game
new_game()
