"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
from scipy.stats._continuous_distns import beta


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    if game.active_player == player:
        return float(len(own_moves) - len(opp_moves))
    else: # It' the opponent's turn, so revise the options a bit
        return float(len([x for x in own_moves if x not in opp_moves]) - len(opp_moves))

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left
        
        options = game.get_legal_moves()
        assert options == legal_moves, "Mismatched moves"
#         print ("\n{}\t\t{}".format(legal_moves, options))

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        _, move = None, None
        try:
            if self.iterative:
                depth, reachedleaf = 0, False
                while not reachedleaf:
                    score, move = self.dosearch(game, depth)
                    print ("Score: {}, Move: {}, Depth: {}".format(score, move, depth))
                    if score == float('inf') or score == float('-inf'):
#                         print ("Reached leaves. Aborting iteration!")
                        reachedleaf = True
                    if self.time_left() < 2*self.TIMER_THRESHOLD:
#                         print ("Reached time limit. Aborting iteration!")
                        break
                    depth += 1
            else:
                _, move = self.dosearch(game, self.search_depth)
        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search
        # (or iterative-deepening search iteration)
#         print ("Returning: {}".format(move))
        return move
    
    def dosearch(self, game, depth):
        if self.method == 'minimax':
            return self.minimax(game, depth)
        else: # alphabeta
            return self.alphabeta(game, depth)

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        legal_moves = game.get_legal_moves(game.active_player)
        if legal_moves and len(legal_moves)>0:
            if depth>0: # Recursive case:
                if maximizing_player:
                    score, move = max([(self.minimax(game.forecast_move(m), depth-1, maximizing_player=False)[0], m) for m in legal_moves])
                else:
                    score, move = min([(self.minimax(game.forecast_move(m), depth-1, maximizing_player=True)[0], m) for m in legal_moves])
            else: # Base case (depth==0)
                return self.score(game, self), []
        else:
            score, move = float('-inf'), (-1, -1)
            
        return score, move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        legal_moves = game.get_legal_moves(game.active_player)
        if legal_moves and len(legal_moves)>0:
            if depth>0: # Recursive case:
                floor = alpha
                ceiling = beta
#                 print ("\tALPHABETA: (({})) {} < score < {}".format(depth, floor, ceiling))
                if maximizing_player:   # MAXIMIZING ply
                    score, move = floor, None
                    for i,m in enumerate(legal_moves):
                        newscore, newmove = self.alphabeta(game.forecast_move(m), depth-1, floor, ceiling, maximizing_player=not maximizing_player)
                        if newmove is None:
                            continue
                        if (move is None and newscore >= score) or (newscore > score):
                            floor, score, move = newscore, newscore, m
#                             print ("\t\tMAXIMIZER (({})): Increased floor ==> {} for siblings after {}".format(depth, floor, i))
                        if score > ceiling: # No need to search any more if we've crossed the upper limit at this max layer already
#                             print ("\t\tMAXIMIZER (({})): Pruned siblings after: {} because ceiling: {} already crossed".format(depth, i, ceiling))
                            break
                else:                   # MINIMIZING ply
                    score, move = ceiling, None
                    for i,m in enumerate(legal_moves):
                        newscore, newmove = self.alphabeta(game.forecast_move(m), depth-1, floor, ceiling, maximizing_player=not maximizing_player)
                        if newmove is None:
                            continue
                        if (move is None and newscore <= score) or (newscore < score):
                            ceiling, score, move = newscore, newscore, m
#                             print ("\t\tMINIMZER (({})): Reduced ceiling ==> {} for siblings after {}".format(depth, ceiling, i)) 
                        if score < floor: # No need to search any more if we've crossed the lower limit at this min layer already
#                             print ("\t\tMINIMIZER (({})): Pruned siblings after: {} because floor: {} already crossed".format(depth, i, floor))
                            break
            else: # Base case (depth==0)
                score, move = self.score(game, self), []
        else:
            score, move = float('-inf'), (-1, -1)

        print ("\tALPHABETA: (({})) Returning {}, {}".format(depth, score, move))
        return score, move