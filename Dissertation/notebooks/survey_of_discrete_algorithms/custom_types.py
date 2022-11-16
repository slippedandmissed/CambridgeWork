from typing import Tuple, List, Callable, Optional, Dict

Vertex = str
Cost = float
CostFunction = Dict[Vertex, Dict[Vertex, Cost]]
Graph = Tuple[List[Vertex], CostFunction]
Solution = List[Vertex]
Solver = Callable[[Graph], Solution]
Optimizer = Callable[[Solver], Solver]
Evaluation = Tuple[Solver, Optional[Optimizer], Graph, Solution, Cost]