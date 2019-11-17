# week 4 project

# Pong

# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = True
RIGHT = False

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]

    # velocity of the ball at the start of the game
    if direction == LEFT:
        #ball_vel = [-random.randrange(120, 240)/60, -random.randrange(60, 180)/60]
        ball_vel = [-4, -4]
    if direction == RIGHT:
        ball_vel = [4, -4]
        #ball_vel = [random.randrange(120, 240)/60, -random.randrange(60, 180)/60]

# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  		# these are ints
    global ball_pos, ball_vel   # lists
    global player_one_score, player_two_score

    paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT

    paddle1_vel = 0
    paddle2_vel = 0

    player_one_score, player_two_score = 0, 0

    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel
    global player_one_score, player_two_score

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 8, 'White', 'White')

    # bounce ball off top and bottom of board
    if (ball_pos[1] + BALL_RADIUS) >= HEIGHT or (ball_pos[1] - BALL_RADIUS) <= 0:
        ball_vel[1] = -ball_vel[1]

    # determine whether paddle and ball collide
    padd1_coverage = [paddle1_pos, paddle1_pos + PAD_HEIGHT]
    padd2_coverage = [paddle2_pos, paddle2_pos + PAD_HEIGHT]

    # ball hits one of the gutters
    if (ball_pos[0] + BALL_RADIUS) >= WIDTH - PAD_WIDTH:
        if ball_pos[1] >= padd2_coverage[0] and ball_pos[1] <= padd2_coverage[1]:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0], ball_vel[1] = ball_vel[0] * 1.10, ball_vel[1] * 1.10
        else:
            spawn_ball(LEFT)
            player_one_score += 1
    if (ball_pos[0] - BALL_RADIUS) <= PAD_WIDTH:
        if ball_pos[1] >= padd1_coverage[0] and ball_pos[1] <= padd1_coverage[1]:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0], ball_vel[1] = ball_vel[0] * 1.10, ball_vel[1] * 1.10
        else:
            spawn_ball(RIGHT)
            player_two_score += 1

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel >= 0 and (paddle1_pos + PAD_HEIGHT) + paddle1_vel <= HEIGHT:
        paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel >= 0 and (paddle2_pos + PAD_HEIGHT) + paddle2_vel <= HEIGHT:
        paddle2_pos += paddle2_vel

    # draw paddles
    pad2_x_cord = WIDTH - PAD_WIDTH
    canvas.draw_polyline([(0, paddle1_pos), (0, paddle1_pos + PAD_HEIGHT)], PAD_WIDTH, 'White')
    canvas.draw_polyline([(pad2_x_cord, paddle2_pos), (pad2_x_cord, paddle2_pos + PAD_HEIGHT)], PAD_WIDTH, 'White')

    # draw scores
    canvas.draw_text(str(player_one_score), (125, 35), 25, 'White')
    canvas.draw_text(str(player_two_score), (450, 35), 25, 'White')

def keydown(key):
    global paddle1_vel, paddle2_vel
    if chr(key) == 'W':
        paddle1_vel = -7
    elif chr(key) == 'S':
        paddle1_vel = 7

    if chr(key) == '&':
        paddle2_vel = -7
    elif chr(key) == '(':
        paddle2_vel = 7

def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel, paddle2_vel = 0 , 0

def button_handler():
    new_game()


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', button_handler, 75)

# start frame
new_game()
frame.start()
