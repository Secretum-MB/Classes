# week 3 project

# Stopwatch Game

# template for "Stopwatch: The Game"
import simplegui
import random

# define global variables
TIME_IN_MS = 0
STOP_ATTEMPTS = 0
STOP_SUCCESSES = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
	if t > 5999:
		timer.stop()
		return "Maxed at 10:00.0"

    milliseconds = str(t % 10)

	seconds_raw = str(t % 600)
	if len(seconds_raw) == 1:
		seconds = "00"
	elif len(seconds_raw) == 2:
		seconds = "0" + seconds_raw[0]
	elif len(seconds_raw) == 3:
		seconds = seconds_raw[:2]

	minutes = str(t // 600)
	return minutes + ':' + seconds + '.' + milliseconds

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
	timer.start()

def stop():
	global STOP_ATTEMPTS, STOP_SUCCESSES, TIME_IN_MS
	if timer.is_running():
		timer.stop()
		STOP_ATTEMPTS += 1

		if TIME_IN_MS % 10 == 0:
			 STOP_SUCCESSES += 1

def reset():
	timer.stop()
	global TIME_IN_MS, STOP_ATTEMPTS, STOP_SUCCESSES
	TIME_IN_MS = 0
	STOP_ATTEMPTS, STOP_SUCCESSES = 0, 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
	global TIME_IN_MS
	TIME_IN_MS += 1

# define draw handler
def draw_handler(canvas):
	canvas.draw_text(format(TIME_IN_MS), [135, 100], 18, 'White')
	canvas.draw_text(str(STOP_SUCCESSES) + '  /  ', [260, 10], 12, 'Red')
	canvas.draw_text(str(STOP_ATTEMPTS), [280, 10], 12, 'White')

# create frame
frame = simplegui.create_frame('Timer Game!', 300, 200)

# register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw_handler)

frame.add_button("Start", start, 75)
frame.add_button("Stop", stop, 75)
frame.add_button("Reset", reset, 75)

# start frame
frame.start()


