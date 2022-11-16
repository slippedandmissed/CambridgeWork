from typing import Tuple, List, Callable, Optional

Vertex = str
Cost = float
Edge = Tuple[Vertex, Vertex, Cost]
Graph = Tuple[List[Vertex], List[Edge]]
Solution = List[Edge]
Solver = Callable[[Graph], Solution]
Optimizer = Callable[[Solver], Solver]
Evaluation = Tuple[Solver, Optional[Optimizer], Graph, Solution, Cost]