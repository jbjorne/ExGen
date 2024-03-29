# The Sliding Puzzle

In the 8-puzzle, at each turn, you can move one of the tiles bordering the empty space into the empty space (that is, there are two or three valid moves at each turn) in order to reach the goal state:

![0.1](SlidingPuzzleGoal.png)

Your goal is to use a heuristic search to move from the starting state N0 towards the goal state in as few moves as possible. The heuristic to use is the [heuristic]().

A search subtree of potential moves is shown below (it does not reach the goal state). Calculating the heuristic values for the nodes, tell in which order of nodes your algorithm traverses the tree in order to reach the best leaf state (An answer could be e.g. of the form [N0,N2,N8](example)). Also show the heuristic values for the listed nodes (e.g. [5](example))

* Nodes in order of traversal: [path](answer)
* Heuristic value for node [n1](): [h1](answer)
* Heuristic value for node [n2](): [h2](answer)
* Heuristic value for node [n3](): [h3](answer)

![0.5](SlidingPuzzleTree.png)