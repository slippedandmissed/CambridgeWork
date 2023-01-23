#!/usr/bin/python3.11

from __future__ import annotations
from typing import Optional, List, Tuple, Any
import math

class Expression:

  parent: Optional[Expression]
  children: List[Expression]

  def __init__(self, parent: Optional[Expression], children: List[Expression]):
    self.parent = parent
    self.children = children
    for child in self.children:
      child.parent = self
  
  def __format__(self, formatstr: str) -> str:
    return format(float(self), formatstr)
  
  def copy(self) -> Expression:
    raise NotImplementedError()

  def subs(self, var: str | Variable, exp: float | int | Expression) -> Expression:
    raise NotImplementedError()

  def simplify(self) -> Expression:
    raise NotImplementedError()
  
  def evaluate(self) -> Any:
    raise NotImplementedError()


class Numerical(Expression):

  def __mul__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Numerical):
      return Multiply(self, other)
    return Multiply(self, Number(other))
  
  def __rmul__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Numerical):
      return Multiply(other, self)
    return Multiply(Number(other), self)

  def __truediv__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Numerical):
      return Divide(self, other)
    return Divide(self, Number(other))
  
  def __rtruediv__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Numerical):
      return Divide(other, self)
    return Divide(Number(other), self)

  def __add__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Numerical):
      return Add(self, other)
    return Add(self, Number(other))
  
  def __radd__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Numerical):
      return Add(other, self)
    return Add(Number(other), self)
  
  def __sub__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Numerical):
      return Add(self, -other)
    return Add(self, Number(-other))
  
  def __rsub__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Numerical):
      return Add(other, -self)
    return Add(Number(other), -self)
  
  def __pow__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Numerical):
      return Pow(self, other)
    return Pow(self, Number(other))
  
  def __rpow__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Numerical):
      return Pow(other, self)
    return Pow(Number(other), self)

  def __neg__(self) -> Numerical:
    return (-1) * self

  def __le__(self, other: float | int | Numerical) -> Conditional:
    if issubclass(type(other), Numerical):
      return Leq(self, other)
    return Leq(self, Number(other))

  def __ge__(self, other: float | int | Numerical) -> Conditional:
    if issubclass(type(other), Numerical):
      return Leq(other, self)
    return Leq(Number(other), self)
  
  def __lt__(self, other: float | int | Numerical) -> Conditional:
    if issubclass(type(other), Numerical):
      return LessThan(self, other)
    return LessThan(self, Number(other))

  def __gt__(self, other: float | int | Numerical) -> Conditional:
    if issubclass(type(other), Numerical):
      return LessThan(other, self)
    return LessThan(Number(other), self)
  
  def __eq__(self, other: float | int | Numerical) -> Conditional:
    if issubclass(type(other), Numerical):
      return Equals(self, other)
    return Equals(self, Number(other))
  
  def __float__(self):
    return float(self.evaluate())

  def evaluate(self) -> float:
    raise NotImplementedError()
    
  def diff(self, var: str | Variable) -> Numerical:
    raise NotImplementedError()


class Number(Numerical):
  value: float

  def __init__(self, value: float, parent: Optional[Expression] = None):
    super().__init__(parent, [])
    self.value = value
  
  def __str__(self) -> str:
    return str(self.value)
  
  def __mul__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Number):
      return Number(self.value * other.value)
    return super().__mul__(other)
  
  def __rmul__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Number):
      return Number(other.value * self.value)
    return super().__rmul__(other)

  def __truediv__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Number):
      return Number(self.value / other.value)
    return super().__truediv__(other)
  
  def __rtruediv__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Number):
      return Number(other.value / self.value)
    return super().__rtruediv__(other)

  def __add__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Number):
      return Number(self.value + other.value)
    return super().__add__(other)

  def __radd__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Number):
      return Number(other.value + self.value)
    return super().__radd__(other)

  def __pow__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Number):
      return Number(self.value ** other.value)
    return super().__pow__(other)

  def __rpow__(self, other: float | int | Numerical) -> Numerical:
    if issubclass(type(other), Number):
      return Number(other.value ** self.value)
    return super().__rpow__(other)

  def __le__(self, other: float | int | Numerical) -> Conditional:
    if issubclass(type(other), Number):
      return Boolean(self.value <= other.value)
    return super().__le__(other)

  def __ge__(self, other: float | int | Numerical) -> Conditional:
    if issubclass(type(other), Number):
      return Boolean(self.value >= other.value)
    return super().__ge__(other)
  
  def __lt__(self, other: float | int | Numerical) -> Conditional:
    if issubclass(type(other), Number):
      return Boolean(self.value < other.value)
    return super().__lt__(other)

  def __gt__(self, other: float | int | Numerical) -> Conditional:
    if issubclass(type(other), Number):
      return Boolean(self.value > other.value)
    return super().__gt__(other)
  
  def __eq__(self, other: float | int | Numerical) -> Conditional:
    if issubclass(type(other), Number):
      return Boolean(self.value == other.value)
    return super().__eq__(other)
  
  def copy(self) -> Numerical:
    return Number(self.value)

  def subs(self, var: str | Variable, exp: float | int | Numerical) -> Numerical:
    return self.copy()
  
  def evaluate(self) -> float:
    return self.value
    
  def diff(self, var: str | Variable) -> Numerical:
    return Number(0)

  def simplify(self) -> Numerical:
    return self.copy()


class Variable(Numerical):
  name: str

  def __init__(self, name: str, parent: Optional[Expression] = None):
    super().__init__(parent, [])
    self.name = name
  
  def __str__(self) -> str:
    return self.name
  
  def copy(self) -> Numerical:
    return Variable(self.name)

  def subs(self, var: str | Variable, exp: float | int | Numerical) -> Numerical:
    if (var.name if issubclass(type(var), Variable) else var) == self.name:
      return exp.copy() if issubclass(type(exp), Numerical) else Number(exp)
    return self.copy()

  def evaluate(self) -> float:
    raise AssertionError(f"Cannot evaluate because variable '{self.name}' is free")
    
  def diff(self, var: str | Variable) -> Numerical:
    return Number(1) if (var.name if issubclass(type(var), Variable) else var) == self.name else Number(0)

  def simplify(self) -> Numerical:
    return self.copy()


class Sine(Numerical):

  def __init__(self, x: Numerical, parent: Optional[Expression] = None):
    super().__init__(parent, [x])
  
  def __str__(self) -> str:
    return f"sin({str(self.children[0])})"
  
  def copy(self) -> Numerical:
    return Sine(self.children[0].copy())

  def subs(self, var: str | Variable, exp: float | int | Numerical) -> Numerical:
    return Sine(self.children[0].subs(var, exp))

  def evaluate(self) -> float:
    return math.sin(self.children[0].evaluate())
    
  def diff(self, var: str | Variable) -> Numerical:
    return self.children[0].diff(var) * Cosine(self.children[0])

  def simplify(self) -> Numerical:
    return Sine(self.children[0].simplify())


class Cosine(Numerical):

  def __init__(self, x: Numerical, parent: Optional[Expression] = None):
    super().__init__(parent, [x])
  
  def __str__(self) -> str:
    return f"cos({str(self.children[0])})"
  
  def copy(self) -> Numerical:
    return Sine(self.children[0].copy())

  def subs(self, var: str | Variable, exp: float | int | Numerical) -> Numerical:
    return Cosine(self.children[0].subs(var, exp))

  def evaluate(self) -> float:
    return math.cos(self.children[0].evaluate())
    
  def diff(self, var: str | Variable) -> Numerical:
    return self.children[0].diff(var) * (-Sine(self.children[0]))

  def simplify(self) -> Numerical:
    return Cosine(self.children[0].simplify())


class Add(Numerical):

  def __init__(self, x: Numerical, y: Numerical, parent: Optional[Expression] = None):
    super().__init__(parent, [x, y])

  def __str__(self) -> str:
    return f"({str(self.children[0])}) + ({str(self.children[1])})"
  
  def copy(self) -> Numerical:
    return Add(self.children[0].copy(), self.children[1].copy())

  def subs(self, var: str | Variable, exp: float | int | Numerical) -> Numerical:
    return Add(self.children[0].subs(var, exp), self.children[1].subs(var, exp))

  def evaluate(self) -> float:
    return self.children[0].evaluate() + self.children[1].evaluate()
    
  def diff(self, var: str | Variable) -> Numerical:
    return self.children[0].diff(var) + self.children[1].diff(var)

  def simplify(self) -> Numerical:
    l_simp = self.children[0].simplify()
    r_simp = self.children[1].simplify()
    if issubclass(type(l_simp), Number) and issubclass(type(r_simp), Number):
      return Number(l_simp.value + r_simp.value)
    return Add(l_simp, r_simp)


class Multiply(Numerical):

  def __init__(self, x: Numerical, y: Numerical, parent: Optional[Expression] = None):
    super().__init__(parent, [x, y])

  def __str__(self) -> str:
    return f"({str(self.children[0])}) * ({str(self.children[1])})"
  
  def copy(self) -> Numerical:
    return Multiply(self.children[0].copy(), self.children[1].copy())

  def subs(self, var: str | Variable, exp: float | int | Numerical) -> Numerical:
    return Multiply(self.children[0].subs(var, exp), self.children[1].subs(var, exp))

  def evaluate(self) -> float:
    return self.children[0].evaluate() * self.children[1].evaluate()
    
  def diff(self, var: str | Variable) -> Numerical:
    return (self.children[0].copy() * self.children[1].diff(var)) + (self.children[0].diff(var) * self.children[1].copy())

  def simplify(self) -> Numerical:
    l_simp = self.children[0].simplify()
    r_simp = self.children[1].simplify()
    if issubclass(type(l_simp), Number) and issubclass(type(r_simp), Number):
      return Number(l_simp.value * r_simp.value)
    return Multiply(l_simp, r_simp)


class Divide(Numerical):

  def __init__(self, x: Numerical, y: Numerical, parent: Optional[Expression] = None):
    super().__init__(parent, [x, y])

  def __str__(self) -> str:
    return f"({str(self.children[0])}) / ({str(self.children[1])})"
  
  def copy(self) -> Numerical:
    return Divide(self.children[0].copy(), self.children[1].copy())

  def subs(self, var: str | Variable, exp: float | int | Numerical) -> Numerical:
    return Divide(self.children[0].subs(var, exp), self.children[1].subs(var, exp))

  def evaluate(self) -> float:
    return self.children[0].evaluate() / self.children[1].evaluate()
    
  def diff(self, var: str | Variable) -> Numerical:
    return Divide(
      Add(
        Multiply(
          self.children[0].diff(var),
          self.children[1].copy()
        ),
        Multiply(
          Number(-1),
          Multiply(
            self.children[0].copy(),
            self.children[1].diff(var)
          )
        )
      ),
      Pow(
        self.children[1].copy(),
        Number(2)
      )
    )

  def simplify(self) -> Numerical:
    l_simp = self.children[0].simplify()
    r_simp = self.children[1].simplify()
    if issubclass(type(l_simp), Number) and issubclass(type(r_simp), Number):
      return Number(l_simp.value / r_simp.value)
    return Divide(l_simp, r_simp)


class NaturalLog(Numerical):

  def __init__(self, x: Numerical, parent: Optional[Expression] = None):
    super().__init__(parent, [x])

  def __str__(self) -> str:
    return f"ln({str(self.children[0])})"
  
  def copy(self) -> Numerical:
    return NaturalLog(self.children[0].copy())

  def subs(self, var: str | Variable, exp: float | int | Numerical) -> Numerical:
    return NaturalLog(self.children[0].subs(var, exp))

  def evaluate(self) -> float:
    return math.log(self.children[0].evaluate())
    
  def diff(self, var: str | Variable) -> Numerical:
    return Divide(self.children[0].diff(var), self.children[0].copy())

  def simplify(self) -> Numerical:
    l_simp = self.children[0].simplify()
    r_simp = self.children[1].simplify()
    if issubclass(type(l_simp), Number) and issubclass(type(r_simp), Number):
      return Number(l_simp.value / r_simp.value)
    return Divide(l_simp, r_simp)


class Pow(Numerical):

  def __init__(self, x: Numerical, y: Numerical, parent: Optional[Expression] = None):
    super().__init__(parent, [x, y])

  def __str__(self) -> str:
    return f"({str(self.children[0])}) ** ({str(self.children[1])})"
  
  def copy(self) -> Numerical:
    return Pow(self.children[0].copy(), self.children[1].copy())

  def subs(self, var: str | Variable, exp: float | int | Numerical) -> Numerical:
    return Pow(self.children[0].subs(var, exp), self.children[1].subs(var, exp))

  def evaluate(self) -> float:
    return self.children[0].evaluate() ** self.children[1].evaluate()
    
  def diff(self, var: str | Variable) -> Numerical:
    return Multiply(
      Pow(
        self.children[0].copy(),
        Add(
          self.children[1].copy(),
          Number(-1)
        )
      ),
      Add(
        Multiply(
          self.children[1].copy(),
          self.children[0].diff(var)
        ),
        Multiply(
          Multiply(
            self.children[0].copy(),
            NaturalLog(
              self.children[0].copy()
            )
          ),
          self.children[1].diff(var)
        )
      )
    )

  def simplify(self) -> Numerical:
    l_simp = self.children[0].simplify()
    r_simp = self.children[1].simplify()
    if issubclass(type(l_simp), Number) and issubclass(type(r_simp), Number):
      return Number(l_simp.value ** r_simp.value)
    return Pow(l_simp, r_simp)


class Conditional(Expression):

  def __and__(self, other: bool | Conditional) -> Conditional:
    if issubclass(type(other), Conditional):
      return And(self, other)
    return And(self, Boolean(other))
  
  def __rand__(self, other: bool | Conditional) -> Conditional:
    if issubclass(type(other), Conditional):
      return And(other, self)
    return And(Boolean(other), self)
  
  def __bool__(self) -> bool:
    return bool(self.evaluate())
    
  def evaluate(self) -> bool:
    raise NotImplementedError()


class Boolean(Conditional):
  
  value: bool

  def __init__(self, value: bool, parent: Optional[Expression]=None):
    self.value = value
    super().__init__(parent, [])
  
  def __str__(self) -> str:
    return str(self.value)
  
  def copy(self) -> Conditional:
    return Boolean(self.value)
  
  def subs(self, var: str | Variable, exp: float | int | Numerical):
    return self.copy()
  
  def evaluate(self) -> bool:
    return self.value
  
  def simplify(self) -> Conditional:
    return self.copy()


class Leq(Conditional):
  
  def __init__(self, x: Numerical, y: Numerical, parent: Optional[Expression]=None):
    super().__init__(parent, [x, y])
  
  def __str__(self) -> str:
    return f"({str(self.children[0])}) <= ({str(self.children[1])})"
  
  def copy(self) -> Conditional:
    return Leq(self.children[0].copy(), self.children[1].copy())
  
  def subs(self, var: str | Variable, exp: float | int | Numerical):
    return Leq(self.children[0].subs(var, exp), self.children[1].subs(var, exp))
  
  def evaluate(self) -> bool:
    return self.children[0].evaluate() <= self.children[1].evaluate()
  
  def simplify(self) -> Conditional:
    l_simp = self.children[0].simplify()
    r_simp = self.children[1].simplify()
    if issubclass(type(l_simp), Number) and issubclass(type(r_simp), Number):
      return Boolean(l_simp.value <= r_simp.value)
    return Leq(l_simp, r_simp)


class LessThan(Conditional):
  
  def __init__(self, x: Numerical, y: Numerical, parent: Optional[Expression]=None):
    super().__init__(parent, [x, y])
  
  def __str__(self) -> str:
    return f"({str(self.children[0])}) < ({str(self.children[1])})"
  
  def copy(self) -> Conditional:
    return LessThan(self.children[0].copy(), self.children[1].copy())
  
  def subs(self, var: str | Variable, exp: float | int | Numerical):
    return LessThan(self.children[0].subs(var, exp), self.children[1].subs(var, exp))
  
  def evaluate(self) -> bool:
    return self.children[0].evaluate() < self.children[1].evaluate()
  
  def simplify(self) -> Conditional:
    l_simp = self.children[0].simplify()
    r_simp = self.children[1].simplify()
    if issubclass(type(l_simp), Number) and issubclass(type(r_simp), Number):
      return Boolean(l_simp.value < r_simp.value)
    return LessThan(l_simp, r_simp)


class Equals(Conditional):
  
  def __init__(self, x: Numerical, y: Numerical, parent: Optional[Expression]=None):
    super().__init__(parent, [x, y])
  
  def __str__(self) -> str:
    return f"({str(self.children[0])}) == ({str(self.children[1])})"
  
  def copy(self) -> Conditional:
    return Equals(self.children[0].copy(), self.children[1].copy())
  
  def subs(self, var: str | Variable, exp: float | int | Numerical):
    return Equals(self.children[0].subs(var, exp), self.children[1].subs(var, exp))
  
  def evaluate(self) -> bool:
    return self.children[0].evaluate() == self.children[1].evaluate()
  
  def simplify(self) -> Conditional:
    l_simp = self.children[0].simplify()
    r_simp = self.children[1].simplify()
    if issubclass(type(l_simp), Number) and issubclass(type(r_simp), Number):
      return Boolean(l_simp.value == r_simp.value)
    return Equals(l_simp, r_simp)


class And(Conditional):

  def __init__(self, x: Conditional, y: Conditional, parent: Optional[Expression]=None):
    super().__init__(parent, [x, y])

  def __str__(self) -> str:
    return f"({str(self.children[0])}) & ({str(self.children[1])})"
  
  def copy(self) -> Conditional:
    return And(self.children[0].copy(), self.children[1].copy())
  
  def subs(self, var: str | Variable, exp: float | int | Numerical):
    return And(self.children[0].subs(var, exp), self.children[1].subs(var, exp))
  
  def evaluate(self) -> bool:
    return self.children[0].evaluate() and self.children[1].evaluate()
  
  def simplify(self) -> Conditional:
    l_simp = self.children[0].simplify()
    r_simp = self.children[1].simplify()
    if issubclass(type(l_simp), Boolean):
      r_simp if l_simp.value else Boolean(False)
    if issubclass(type(r_simp), Boolean):
      l_simp if r_simp.value else Boolean(False)
    return And(l_simp, r_simp)


class Piecewise(Numerical):

  nums: List[Numerical]
  conds: List[Conditional]

  def __init__(self, *pieces: List[Tuple[float | int | Numerical, bool | Conditional]], parent: Optional[Expression] = None):
    self.nums = []
    self.conds = []
    for num, cond in pieces:
      self.nums.append(num if issubclass(type(num), Numerical) else Number(num))
      self.conds.append(cond if issubclass(type(cond), Conditional) else Boolean(cond))
    super().__init__(parent, self.nums + self.conds)

  def __str__(self) -> str:
    return f"Piecewise([{', '.join('('+str(num)+', '+str(cond)+')' for num, cond in zip(self.nums, self.conds))}])"
  
  def copy(self) -> Numerical:
    return Piecewise(*((num.copy(), cond.copy()) for num, cond in zip(self.nums, self.conds)))

  def subs(self, var: str | Variable, exp: float | int | Numerical) -> Numerical:
    return Piecewise(*((num.subs(var, exp), cond.subs(var, exp)) for num, cond in zip(self.nums, self.conds)))

  def evaluate(self) -> float:
    for num, cond in zip(self.nums, self.conds):
      if cond.evaluate():
        return num.evaluate()
    print("Warning: no conditions match")
    return 0
    
  def diff(self, var: str | Variable) -> Numerical:
    return Piecewise(*((num.diff(var), cond.copy()) for num, cond in zip(self.nums, self.conds)))

  def simplify(self) -> Numerical:
    simp_pieces = []
    for num, cond in zip(self.nums, self.conds):
      simp_cond = cond.simplify()
      if issubclass(type(simp_cond), Boolean):
        if simp_cond.value and len(simp_pieces) == 0:
          return num.simplify()
        else:
          continue
      simp_pieces.append((num.simplify(), simp_cond))
    return Piecewise(*simp_pieces)

def symbols(names: str) -> List[Variable]:
  syms = list(Variable(x) for x in names.strip().split(" "))
  return syms if len(syms) > 1 else syms[0]

def sin(x: float | int | Numerical) -> Sine:
  return Sine(x if issubclass(type(x), Numerical) else Number(x))

def cos(x: float | int | Numerical) -> Cosine:
  return Cosine(x if issubclass(type(x), Numerical) else Number(x))

def ln(x: float | int | Numerical) -> NaturalLog:
  return NaturalLog(x if issubclass(type(x), Numerical) else Number(x))
