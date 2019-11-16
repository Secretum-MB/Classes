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
NTRIALS = 3         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

# Add your functions here.

def mc_trial(board, player):
    while game.check_win() == None:
        possible_moves = game.get_empty_squares()
        selected_move = random.choice(possible_moves)
        game.move(selected_move[0], selected_move[1], player)
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    if game.check_win() == player:
        for row in range(game.get_dim()):
            for col in range(game.get_dim()):
                if game.square(row, col) == player:
                    scores[row][col] += SCORE_CURRENT
                elif game.square(row, col) != 1:
                    scores[row][col] -= SCORE_OTHER
    else:
        opponent = provided.switch_player(player)
        if game.check_win() == opponent:
            for row in range(game.get_dim()):
                for col in range(game.get_dim()):
                    if game.square(row, col) == opponent:
                        scores[row][col] += SCORE_CURRENT
                    elif game.square(row, col) != 1:
                        scores[row][col] -= SCORE_OTHER

def get_best_move(board, scores):
    highest_score = 0
    best_choices = []
    possible_moves = game.get_empty_squares()
    for empty in possible_moves:
        if scores[empty[0]][empty[1]] >= highest_score:
            best_choices.append(empty)
            highest_score = scores[empty[0]][empty[1]]
    return random.choice(best_choices)

def mc_move(board, player, trials):
    # should this function initialize new games..
    for trial in range(trials):
        mc_trial(board, player)
        mc_update_scores(scores, board, player)

        print(game.clone())
        print(scores)
    print(get_best_move(board, scores))



#dim = 3
#game = provided.TTTBoard(dim)
#scores = [[0 for col in range(dim)] for j in range(dim)]

#mc_trial(game.clone(), provided.PLAYERX)
#mc_update_scores(scores, game.clone(), provided.PLAYERX)
#get_best_move(game.clone(), scores)
#mc_move(game.clone(), provided.PLAYERX, NTRIALS)


# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
