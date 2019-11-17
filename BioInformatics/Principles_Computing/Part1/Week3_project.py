# principles of computing
# week 3: project
# Monti-Carlo simulation: Tick-Tak-Toe

"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100        # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

# Add your functions here.

def mc_trial(board, player):
    "completes game from board state using random moves for both players"
    while board.check_win() == None:
        possible_moves = board.get_empty_squares()
        selected_move = random.choice(possible_moves)
        board.move(selected_move[0], selected_move[1], player)
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    "scores each square of a completed game"
    if board.check_win() == player:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row, col) == player:
                    scores[row][col] += SCORE_CURRENT
                elif board.square(row, col) != 1:
                    scores[row][col] -= SCORE_OTHER
    else:
        opponent = provided.switch_player(player)
        if board.check_win() == opponent:
            for row in range(board.get_dim()):
                for col in range(board.get_dim()):
                    if board.square(row, col) == opponent:
                        scores[row][col] += SCORE_CURRENT
                    elif board.square(row, col) != 1:
                        scores[row][col] -= SCORE_OTHER

def get_best_move(board, scores):
    "given game state, determine best move"
    highest_score = None
    best_choices = []
    possible_moves = board.get_empty_squares()
    for empty in possible_moves:
        if scores[empty[0]][empty[1]] > highest_score or \
           highest_score is None:
            best_choices = [empty]
            highest_score = scores[empty[0]][empty[1]]
        elif scores[empty[0]][empty[1]] == highest_score:
            best_choices.append(empty)
    best_choice = random.choice(best_choices)
    return best_choice

def mc_move(board, player, trials):
    "uses monti-carlo simulation to find best move for computer"
    scores = [[0 for col in range(board.get_dim())] \
              for j in range(board.get_dim())]
    game_state = scores[:]
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            game_state[row][col] = board.square(row, col)

    for trial in range(trials):
        game = provided.TTTBoard(dim=board.get_dim(), board=game_state)
        mc_trial(game, player)
        mc_update_scores(scores, game.clone(), player)

    return get_best_move(board, scores)


# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
