# Alpha Go Highlights

## Overview

Alpha Go is the most advanced game playing agent that has been built; a culmination of a sequence of progressively more advanced game playing agents, the last famous one being Deep Mind (2) which defeated the reigning chess champion at the time — Gary Kasparov — in 1997. Subsequently, there have been numerous technological advancements that have pushed the envelope on computer game playing. Not only has computational power increased exponentially (to gather, store and process vastly larger swathes of data in vastly decreased time scales) in line with Moore’s Law, but so have various new game playing (or supportive) methodologies/algorithms, most notably Neural Networks.

The aforementioned progression of agents started with simple game tree search algorithms (such as Minimax search) for simple tree games such as Tic-Tac-Toe. Next came alpha/beta pruning, as with the chess-playing Deep Blue, followed then by Alpha Go — a programmatically less convoluted game playing agent relying on technologies like Monte Carlo Tree Search and Neural Networks, achieving far better performance than was thought possible at the time.

2016, the year that Alpha Go first defeat the reigning champion of the time -- Lee Sudel -- was an inflection point for renewed industry interest in Artificial Intelligence, particularly in the sub-domain of Deep Learning, which has shown tremendous promise as an alternative to other machine learning-based technologies. This document summarizes the salient aspects of the Alpha Go agent, while also differentiating it from the previous Deep Blue agent.

## Challenges

Though alpha/beta pruning was an efficient tree search algorithm, achieving faster search through the game tree than minimax, it was not useful with Go. This is because such strategies were useful when playing perfect-play games (i.e, games wherein the number of possibilities were large but still searchable). In contrast, Go has many more possible moves at each step (~250), and a deeper game play (~300 moves), rendering minimax exploration of the game tree intractable.

Furthermore, no evaluation function existed at the time of Deep Blue that could predict the efficacy of a given Go game state, precisely because the possibilities for the game to subsequently change, were endless.

## Strategy

What was needed, at a minimum, was a stochastic approach to game tree search, wherein each move that was available at a node could be explored through a ‘random’ selection process, vastly trimming down the search space. This is what Monte Carlo Tree Search does. More specifically, every player’s move generally involves a sequence of steps, including Selection, Expansion, Simulation and Back-propagation. Each time a move is played, through mere probabilistic inference, a policy of selecting the ‘best’ move …..

But what really made Alpha Go shine is not the Monte Carlo Tree Search, but rather, the use of Neural Networks to step in for the otherwise random selection stage, and the evaluation function. This was achieved by first training 3 neural networks to play the entire Go game purely based on the state of the current board as input on each move, without any search. Three types of neural networks - called policy networks — were trained, as below:

*Policy network (Supervised):*
- Training: 30 million amateur matches
- Goal: Predict the next move.
- Accuracy: 57% accuracy in casual tournaments.
- Performance: 3ms per response.

*Policy network (Reinforced):* (Copied from 1st network as-is and further trained)
- Training: Network played itself 1.2 million times
- Goal: Predict the best move:
- Accuracy: 85% accuracy against an existing Go playing AI (Pachi). 
- Performance: 3ms per response.

*Fast Rollout Policy network:*
- Goal: Fast move. Trimmed down version of above.
- Performance: 2 micro seconds per response. Much faster.

Another neural network, called the _Value Network_, was trained to play Go purely as a sort of evaluation function that assigns scores to each of the possible moves, of which the agent can choose the highest:
- Training: Same 30 million amateur matches + self play
- Goal: Evaluation weight of the win based on current board
- Performance: 77% accuracy
- Accuracy: Determining best move based on highest evaluation value from possible moves. Beats strongest existing AI solutions for Go.

The key development that launched AlphaGo to an even higher level of game play was the _combined_ use of the MCTS and the aforementioned networks, as follows:
- Policy network: Pick current best moves (sampling)
- Value network: Prune the sampled list
- Fast rollout: Guide the simulation phase (as often as possible)

## Conclusion

Distributed Alpha Go — running on 1202 CPUs and 176 GPUs — won 4 out of 5 matches against Lee Sedul, all without ever being spoon-fed an evaluation function or set of game strategies, nor using any lookup database with minimax search the way Deep Blue had been programmed. In fact, no Go-specific logic had been programmed into AlphaGo. It learned everything, on its own, by "watching others", and "self-play”. It has been termed the biggest breakthrough in AI thus far. Furthermore, it relied on CPUs and GPUs as hardware. With the introduction of TPUs (Tensor Processing Units) since then, the performance of such agents will only exceed that of the past.

The implementation of the Isolation game in this repository, however, has a less ambitious and humbler agenda. More specifically, it utilizes a similar approach as did the Deep Blue game agent, such as alpha/beta and minimax tree search, time-limited iterative deepening, quiessant search and a choice of a few evaluation functions of varying efficacy.
