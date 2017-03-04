'''
Created on Mar 4, 2017

@author: safdar
'''

from collections import namedtuple

from isolation import Board
from sample_players import RandomPlayer
from sample_players import null_score
from sample_players import open_move_score
from sample_players import improved_score
from game_agent import CustomPlayer
from game_agent import custom_score
from isolation.visualizer import Visualizer
import random

Agent = namedtuple("Agent", ["player", "name"])

def mymain():
    mm_null_reg_agent = Agent(CustomPlayer(score_fn=null_score, method='minimax', search_depth=3, iterative=False), "mm_null_reg_agent")
    mm_open_reg_agent = Agent(CustomPlayer(score_fn=open_move_score, method='minimax', search_depth=3, iterative=False), "mm_open_reg_agent")
    mm_impr_reg_agent = Agent(CustomPlayer(score_fn=improved_score, method='minimax', search_depth=3, iterative=False), "mm_impr_reg_agent")
    mm_cstm_reg_agent = Agent(CustomPlayer(score_fn=custom_score, method='minimax', search_depth=3, iterative=False), "mm_cstm_reg_agent")
    ab_null_reg_agent = Agent(CustomPlayer(score_fn=null_score, method='alphabeta', search_depth=3, iterative=False), "ab_null_reg_agent")
    ab_open_reg_agent = Agent(CustomPlayer(score_fn=open_move_score, method='alphabeta', search_depth=3, iterative=False), "ab_open_reg_agent")
    ab_impr_reg_agent = Agent(CustomPlayer(score_fn=improved_score, method='alphabeta', search_depth=3, iterative=False), "ab_impr_reg_agent")
    ab_cstm_reg_agent = Agent(CustomPlayer(score_fn=custom_score, method='alphabeta', search_depth=3, iterative=False), "ab_cstm_reg_agent")
    ab_null_id_agent = Agent(CustomPlayer(score_fn=null_score, method='alphabeta', search_depth=3, iterative=True), "ab_null_id_agent")
    ab_open_id_agent = Agent(CustomPlayer(score_fn=open_move_score, method='alphabeta', search_depth=3, iterative=True), "ab_open_id_agent")
    ab_impr_id_agent = Agent(CustomPlayer(score_fn=improved_score, method='alphabeta', search_depth=3, iterative=True), "ab_impr_id_agent")
    ab_cstm_id_agent = Agent(CustomPlayer(score_fn=custom_score, method='alphabeta', search_depth=3, iterative=True), "ab_cstm_id_agent")

    # Game 1:
    game1 = Board(ab_cstm_reg_agent.player, mm_impr_reg_agent.player)
    
    # Initial location:
    move = random.choice(game1.get_legal_moves())
    game1.apply_move(move)
    move = random.choice(game1.get_legal_moves())
    game1.apply_move(move)
    
    winner, moves, reason = game1.play()
    print (game1.to_string())
    print ("Replaying moves...")
    print (moves)
    visualizer = Visualizer(ab_cstm_reg_agent.name, mm_impr_reg_agent.name, moves)
    visualizer.play()
    visualizer.quit()

if __name__ == "__main__":
    mymain()
