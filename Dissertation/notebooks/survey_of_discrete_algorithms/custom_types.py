from typing import Tuple, List, Callable

Vertex = str
Cost = float
Edge = Tuple[Vertex, Vertex, Cost]
Graph = Tuple[List[Vertex], List[Edge]]
Solution = List[Edge]
Solver = Callable[[Graph], Solution]
Evaluation = Tuple[Solver, Graph, Solution, Cost]
