#!/usr/bin/python3.9

from pptree import print_tree
from copy import deepcopy
from io import StringIO
import numpy as np
import sys

real_stdout = sys.stdout

class Tree:
  def __init__(self, name="", children=None):
    self.name = name
    self.children = [] if children is None else children
    self.score = {}
    for k in "ACTG":
      self.score[k] = {}

  def __str__(self):
      sys.stdout = my_stdout = StringIO()
      print_tree(self, childattr="children", nameattr="name", horizontal=False)
      s = my_stdout.getvalue()
      sys.stdout = real_stdout
      return s
    
  
  def s(self, i, v):
    if v not in self.score[i]:
      if v.name != "":
        self.score[i][v] = 0 if i == v.name else np.inf
      
      else:
        opts = np.array([self.s(j, x) + δ(i,j) for x in v.children for j in self.score.keys()])
        self.score[i][v] = np.min(opts)

    return self.score[i][v]
  
  def all_nodes(self):
    yield self
    for l in self.children:
      for c in l.all_nodes():
        yield c
  
  def small_parsimony(self):
    tree = deepcopy(self)
    for k in tree.score.keys():
      tree.s(k, tree)
    for v in tree.all_nodes():
      s = [tree.score[k][v] for k in tree.score.keys()]
      v.name = list(tree.score.keys())[np.argmin(s)]
    return tree


def δ(i, j):
  return 0 if i == j else 1

x = Tree(children=[
  Tree(children=[
    Tree(children=[
      Tree("G"),
      Tree("G")
    ]),
    Tree(children=[
      Tree("T"),
      Tree("G")
    ])
  ]),
  Tree(children=[
    Tree(children=[
      Tree("G"),
      Tree("G")
    ]),
    Tree(children=[
      Tree("T"),
      Tree("G")
    ])
  ])
])

print(x.small_parsimony())