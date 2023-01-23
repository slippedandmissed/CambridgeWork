import sympy
from typing import Iterable, Tuple, Callable

CostFunction = sympy.core.expr.Expr
City = Tuple[float, float]
Instance = Tuple[CostFunction, Iterable[City]]
Solution = Tuple[sympy.core.expr.Expr, sympy.core.expr.Expr]
Polygon = Iterable[Tuple[float, float]]
Solver = Callable[[Instance], Solution]