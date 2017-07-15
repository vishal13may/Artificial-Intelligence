# Artificial Intelligence Exercises
## Alpha Beta Pruning
* Problem Statement: Write a program to determine the minimax value for given positions of the Reversi game, using the Alpha-Beta pruning algorithm with positional weight evaluation functions.
* Rules of the Reversi game were as per: [Wiki Page](https://en.wikipedia.org/wiki/Reversi)
* The program will take the input from the file input.txt, and print out its output to the file output.txt. Each input of the program contains a game position (including the board state and the player to move) and a search cut-off depth D, and the program should output the corresponding information after running an Alpha-Beta search of depth D.

```
Input format:
<player to move>
<search cut-off depth>
<current board status>
where the board status is denoted by * as blank cell, X as black piece, and O as white piece.

Output format:
<next state>
<traverse log>
where the traverse log requires 5 columns. Each column is separated by “,”. The five columns are node, depth, minimax value, alpha, beta.
```
  
## Resolution
* Problem Statement: Suppose you have a wedding to plan, and want to arrange the wedding seating for a certain number of guests in a hall. The hall has a certain number of tables for seating. Some pairs of guests are couples or close Friends (F) and want to sit together at the same table. Some other pairs of guests are Enemies (E) and must be separated into different tables. The rest of the pairs are Indifferent (I) to each other and do not mind sitting together or not. However, each pair of guests can have only one relationship, (F), (E) or (I). Find a seating arrangement that satisfies all the constraints.
* Implemented DPLL algorithm to act as a SAT solver for smaller inputs.

```
Input Format:
4 2
1 2 F
2 3 E
The first line contains two integers denoting the number of guests \<M\> and the number of tables \<N\> respectively. Each line following contains two integers representing the indices of a pair of guests and one character indicating whether they are Friends (F) or Enemies (E).
The rest of the pairs are indifferent by default.

Sample Output
yes
1 2
2 2
3 1
4 1
A single line output yes/no to indicate whether the sentence is satisfiable or not. If the sentence can be satisfied, output yes in the first line, and then provide just one of the possible solutions. (Note that there may be more than one possible solution, but again, your task is to provide only one of them.) Each line after “yes” contains the assigned table for a specific guest for the solution.
```

## Utility using Decision Network
* Problem Statement: Given a decision network, which may have several decision nodes, several chance nodes, and at most one utility node, answer the following queries:
  * Calculate a specific joint, marginal, or conditional probability.
  * Calculate the expected utility of a particular decision, or determine the decision with the maximum expected utility.
* Implemented caching to optimize the time required to obtain the solution (less than 2 seconds run time for a decision tree up to depth 30).

```
Input Format:
P(D = + | L = -, I = +)
EU(I = +)
EU(I = + | L = +)
MEU(I)
MEU(I | L = +)
******
L
0.4
***
N | L
0.8 +
0.3 -
***
I
decision
***
D | N I
0.3 + +
0.6 + -
0.95 - +
0.05 - -
******
utility | D
100 +
-10 -

Each line before the “******” will contain a single query. The query can have three forms, signaled by the function name beginning the query:
1)	Queries beginning with “P” are asking for a specific joint, marginal, or conditional probability.
2)	Queries beginning with “EU” are asking for expected utility over one or more decision nodes, conditioned on the given observed evidence.
3)	Queries beginning with “MEU” are asking for maximum expected utility over one or more decision nodes, conditioned on the given observed evidence.
The line after all queries will have six “*” as the separator. 
The lines following the separator represent the Bayesian or decision network by showing the tables of probabilities / conditional probabilities for each node.
Each tables is separated by a line with three asterisks (“***”), and will have the following format:
e.g.
D | N I
0.3 + +
0.6 + -
0.9 - +
0.05 - -
The first line contains the node’s name. If the node has any parents, its name will be followed by a “|” and then the names of its parents (all separated by spaces).
All nodes can have only two values, “+” (True) or “−” (False).
```
