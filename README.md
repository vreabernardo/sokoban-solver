# Sokoban Solver

<p align="center">
    <img src="https://github.com/vreabernardo/sokoban-solver/assets/45080358/359ab3d7-98ae-47fd-8d88-d84f1ec014f2" width="55%" />
  </p>

## Overview

This repository is dedicated to the development of a Sokoban puzzle solver using a variety of algorithms, including Reinforcement Learning (RL), Breadth-First Search (BFS), Depth-First Search (DFS), Uniform Cost Search (UCS), and A* (A Star Search). 

Let's dive into the project's objectives and why it's an exciting challenge.

## Project Goals

### Solving Sokoban Puzzles

The primary goal of this project is to create a Sokoban puzzle solver capable of finding optimal solutions for a wide range of Sokoban puzzles. Sokoban puzzles are transportation puzzles where the player must push boxes to designated storage locations within a room. The simplicity of the goal belies the complexity that can arise due to the maze-like nature of the puzzles.

### Challenges

The possibility of making irreversible mistakes makes these puzzles so challenging especially for Reinforcement Learning algorithms, which mostly lack the ability to think ahead.

### Leveraging Multiple Algorithms

To tackle the diverse challenges posed by Sokoban puzzles, we are exploring various algorithmic approaches:

1. **Reinforcement Learning (RL)**: We are developing an RL-based agent to learn optimal strategies for solving Sokoban puzzles. This involves training the agent to make intelligent decisions while considering the long-term consequences of its actions.

2. **Breadth-First Search (BFS)**: BFS is a classic graph search algorithm that explores all possible paths systematically. We'll implement BFS to find solutions for Sokoban puzzles by exploring the state space.

3. **Depth-First Search (DFS)**: DFS is another graph search algorithm that delves deep into a path before backtracking. We'll use DFS to explore Sokoban puzzle states and find potential solutions.

4. **Uniform Cost Search (UCS)**: UCS is a variant of Dijkstra's algorithm, which prioritizes paths based on their cost. We'll apply UCS to find the least costly solutions to Sokoban puzzles.

5. **A* (A Star Search)**: A* is a heuristic search algorithm that balances the cost of the path and an estimate of the remaining cost to reach the goal. We'll implement A* to efficiently solve Sokoban puzzles.
