'''
Created on Mar 4, 2017

@author: safdar
'''

from collections import namedtuple

from isolation import Board
from sample_players import RandomPlayer
from scorefunctions import null_score, net_mobility_score
from scorefunctions import open_move_score
from scorefunctions import improved_score
from scorefunctions import net_advantage_score
from scorefunctions import custom_score
from game_agent import CustomPlayer
import warnings
from isolation.visualizer import Visualizer
import random

TIME_LIMIT = 200
NUM_MATCHES = 5
VISUALIZE = True
Agent = namedtuple("Agent", ["player", "name"])

def tryall():
    # Setup all the permutations
    search_depths = [3, 5]
    score_functions = [null_score, open_move_score, improved_score, custom_score]
    methods = ["minimax", "alphabeta"]
    iteratives = [False, True]
    
    # Setup the players:
    player1_agents = []
    player2_agents = [Agent(RandomPlayer(), "random_player")]
    for score_function in score_functions:
        for method in methods:
            for iterative in iteratives:
                for search_depth in search_depths:
                    params = {"search_depth": search_depth, "method": method, "iterative": iterative, "score_fn": score_function}
                    name = "{:16s} / {:9s} / DEPTH({:1d}) / ITER({:1b})".format(score_function.__name__, method, search_depth, iterative)
                    if score_function is improved_score or score_function is custom_score:
                        player1_agents.append(Agent(CustomPlayer(**params), name))
                    else:
                        player2_agents.append(Agent(CustomPlayer(**params), name))
                    
    # Launch the matches for each pair:
    counter = 0
    for player1 in player1_agents:
        for player2 in player2_agents:
            counter += 1
            # Play some games:
            wins = 0.
            num_wins = {player1: 0, player2: 0}
            num_timeouts = {player1: 0, player2: 0}
            num_invalid_moves = {player1: 0, player2: 0}
            print("{:2d}: {:50s}\t--VS--\t {:50s}".format(counter, player1.name, player2.name), end=' ')
            for _ in range(0, NUM_MATCHES):
                games = [Board(player1.player, player2.player), Board(player2.player, player1.player)]
                
                # initialize both games with a random move and response
                for _ in range(2):
                    move = random.choice(games[0].get_legal_moves())
                    games[0].apply_move(move)
                    games[1].apply_move(move)
            
                # play both games and tally the results
                for game in games:
                    winner, moves, termination = game.play(time_limit=TIME_LIMIT)
                    if player1.player == winner:
                        num_wins[player1] += 1
                        if termination == "timeout":
                            num_timeouts[player2] += 1
                        else:
                            num_invalid_moves[player2] += 1
                    elif player2.player == winner:
                        num_wins[player2] += 1
                        if termination == "timeout":
                            num_timeouts[player1] += 1
                        else:
                            num_invalid_moves[player1] += 1
            winratio = 100 * (num_wins[player1] / (num_wins[player1] + num_wins[player2]))
            print("==>: Wins {:3.0f} % {:5s} ({:2d} to {:2d}) / Timeouts ({:2d} to {:2d})".\
                  format(winratio, \
                         "..|  " if winratio <= 50 else "  |..", \
                         int(num_wins[player1]), int(num_wins[player2]), \
                         int(num_timeouts[player1]), int(num_timeouts[player1])))

def mymain():
    visualizing = False
#     mm_null_reg_agent = Agent(CustomPlayer(score_fn=null_score, method='minimax', search_depth=3, iterative=False), "mm_null_reg_agent")
#     mm_open_reg_agent = Agent(CustomPlayer(score_fn=open_move_score, method='minimax', search_depth=3, iterative=False), "mm_open_reg_agent")
#     mm_impr_reg_agent = Agent(CustomPlayer(score_fn=improved_score, method='minimax', search_depth=3, iterative=False), "mm_impr_reg_agent")
#     mm_cstm_reg_agent = Agent(CustomPlayer(score_fn=custom_score, method='minimax', search_depth=3, iterative=False), "mm_cstm_reg_agent")
#     ab_null_reg_agent = Agent(CustomPlayer(score_fn=null_score, method='alphabeta', search_depth=5, iterative=False), "ab_null_reg_agent")
#     ab_open_reg_agent = Agent(CustomPlayer(score_fn=open_move_score, method='alphabeta', search_depth=3, iterative=False), "ab_open_reg_agent")
#     ab_impr_reg_agent = Agent(CustomPlayer(score_fn=improved_score, method='alphabeta', search_depth=3, iterative=False), "ab_impr_reg_agent")
#     ab_cstm_reg_agent = Agent(CustomPlayer(score_fn=custom_score, method='alphabeta', search_depth=3, iterative=False), "ab_cstm_reg_agent")
#     ab_null_id_agent = Agent(CustomPlayer(score_fn=null_score, method='alphabeta', search_depth=3, iterative=True), "ab_null_id_agent")
#     ab_open_id_agent = Agent(CustomPlayer(score_fn=open_move_score, method='alphabeta', search_depth=3, iterative=True), "ab_open_id_agent")
#     ab_impr_id_agent = Agent(CustomPlayer(score_fn=improved_score, method='alphabeta', search_depth=3, iterative=True), "ab_impr_id_agent")
#     ab_cstm_id_agent = Agent(CustomPlayer(score_fn=custom_score, method='alphabeta', search_depth=3, iterative=True), "ab_cstm_id_agent")

    player1 = Agent(CustomPlayer(score_fn=net_mobility_score, method='alphabeta', search_depth=3, iterative=True), "Custom")
    player2 = Agent(CustomPlayer(score_fn=improved_score, method='alphabeta', search_depth=3, iterative=True), "Improved")


    # Play a few games:
    for i in range (0, 5):
        game1 = Board(player1.player, player2.player)
        game2 = Board(player2.player, player1.player)
        
        # Initial location:
        move = random.choice(game1.get_legal_moves())
        game1.apply_move(move)
        game2.apply_move(move)
        move = random.choice(game1.get_legal_moves())
        game1.apply_move(move)
        game2.apply_move(move)
        
        winner1, moves1, reason1 = game1.play()
        winner1 = 1 if player1.player == winner1 else 2
        winner2, moves2, reason2 = game2.play()
        winner2 = 1 if player1.player == winner2 else 2
        print ("Player {} won game 1. Reason: {}".format(winner1, reason1))
        print ("Player {} won game 2. Reason: {}".format(winner2, reason2))
        
        if visualizing:
            print ("Replaying moves for game 1...")
            print (moves1)
            visualizer = Visualizer(player1.name, player2.name, moves1)
            visualizer.play()
            visualizer.quit()
            print ("Replaying moves for game 2...")
            print (moves2)
            visualizer = Visualizer(player2.name, player1.name, moves2)
            visualizer.play()
            visualizer.quit()

        print ("Done")
        
if __name__ == "__main__":
    mymain()
