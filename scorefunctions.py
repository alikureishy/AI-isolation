'''
Created on Mar 5, 2017

@author: safdar
'''

INFINITY = float('inf')


def null_score(game, player):
    """This heuristic presumes no knowledge for non-terminal states, and
    returns the same uninformative value for all other states.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return 0.


def open_move_score(game, player):
    """The basic evaluation function described in lecture that outputs a score
    equal to the number of moves open for your computer player on the board.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)))


def improved_score(game, player):
    """The "Improved" evaluation function discussed in lecture that outputs a
    score equal to the difference in the number of moves available to the
    two players.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)

#################################################################
#                    CUSTOM SCORING ATTEMPTS                    #
#################################################################
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
    return net_advantage_score(game, player)

def staged_score(game, player):
    # Strategy:
    # - First half: Stay near center + stay away from other
    # - Second half: Stay close + offensive + net_mobility
    # - Third half: net_advantage
    stage = game_stage(game)
    if stage <= 33.0:
        return combo_nearcenter_avoidopponent_score(game, player)
    elif stage <= 66.0:
        return combo_offensive_nearopponent_netmobility_score(game, player)
    else:
        return combo_netadvantage_nearopponent_score(game, player)

def combo_nearcenter_avoidopponent_score(game, player):
    score = 0.
    score += accessibility_score(game, player)
    score -= proximity_score(game, player)
    return score

def combo_offensive_nearopponent_netmobility_score(game, player):
    score = 0.
    score += offensive_score(game, player)
    score += proximity_score(game, player)
    return score

def combo_netadvantage_nearopponent_score(game, player):
    score = 0.
    score += net_advantage_score(game, player)
    score += offensive_score(game, player)
    return score

def game_stage(game):
    total_spaces = game.width * game.height
    remaining_spaces = game.get_blank_spaces_count()
    assert total_spaces >= remaining_spaces
    percent_remaining = 100 * ((total_spaces - remaining_spaces) / total_spaces)
    return 100 - percent_remaining

# Number of hops between two positions on the board
def gethopdistance(x, y):
    dx = abs(x[0] - y[0])
    dy = abs(x[1] - y[1])
    delta = max(dx, dy)//2
    return delta

# Just check if the player won or lose, or neither
def winlose_score(game, player):
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    return 0

def net_advantage_score(game, player):
    score = winlose_score(game, player)
    if -INFINITY < score < INFINITY:
        own_moves = game.get_legal_moves(player)
        opp_moves = game.get_legal_moves(game.get_opponent(player))
        if game.active_player == player:
            score += float(len(own_moves) - len(opp_moves))
        else: # It' the opponent's turn, so revise the options a bit
            score += float(len([x for x in own_moves if x not in opp_moves]) - len(opp_moves))
    return score

# Has more move options than opponent
def net_mobility_score(game, player):
    score = winlose_score(game, player)
    if -INFINITY < score < INFINITY:
        own_moves = len(game.get_legal_moves(player))
        opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
        if player == game.active_player:
            if own_moves > opp_moves:
                score += 2              # Active player so extra adv
            elif own_moves < opp_moves:
                score -= 1
        else:
            # Having fewer moves is worse if we're not the next player
            if own_moves > opp_moves:
                score += 1
            elif own_moves < opp_moves: # Not active, so worse-off
                score -= 2
    return score
    
# Has overlap with opponent's next options
def offensive_score(game, player):
    score = winlose_score(game, player)
    if -INFINITY < score < INFINITY:
        own_moves = game.get_legal_moves(player)
        opp_moves = game.get_legal_moves(game.get_opponent(player))
        current_overlap = [x for x in own_moves if x in opp_moves]
        if player == game.active_player:
            if len(current_overlap) > 0:
                score += 1  # We are at an advantage
        else:
            if len(current_overlap) > 0:
                score -= 1  # We are at a disadvantage
    return score

# Distance from the center of the board
def accessibility_score(game, player):
    score = winlose_score(game, player)
    if -INFINITY < score < INFINITY:
        center = (round(game.height / 2), round(game.width / 2))
        own_location = game.get_player_location(player)
        delta = gethopdistance(own_location, center)
        if delta < round(center[0]/2):
            score += 1
        elif delta > round(center[0]/2):
            score += -1
            
    return score

# Distance from the patches of open spaces. Tryes to avoid the horizon problem.
# def horizon_score(game, player):
#     score = winlose_score(game, player)
#     if -INFINITY < score < INFINITY:
#         own_moves = len(game.get_legal_moves(player))
#         opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
#         opp_location = game.get_player_location(game.get_opponent(player))
#         blank_spaces = game.get_blank_spaces()
#         x = round(sum(map(lambda x: x[0], blank_spaces)) / len(blank_spaces))
#         y = round(sum(map(lambda x: x[1], blank_spaces)) / len(blank_spaces))
#         centroid = (x, y)
#         total_moves = own_moves + opp_moves
#     return score

# Proximity from each other: Closer = higher
def proximity_score(game, player):
    score = winlose_score(game, player)
    if -INFINITY < score < INFINITY:
        own_location = game.get_player_location(player)
        opp_location = game.get_player_location(game.get_opponent(player))
        delta = gethopdistance(own_location, opp_location)
        score -= delta   # Since the knight moves in an L shape (so can jump 2 spaces net)
    return score

