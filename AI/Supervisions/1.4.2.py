import numpy as np

class Tree:
	def __init__(self, value=None, children=[]):
		self.children = children
		self.value = value

	def __str__(self):
		c = list(str(x).split("\n") for x in self.children)
		v = "" if self.value is None else str(self.value)
		n = len(c)

		if n > 3:
			return "I don't know how to print this :("

		if n == 0:
			return v

		tlen = sum(len(x[0]) for x in c) + n - 1

		s = v.center(tlen, " ") + "\n"
		if n == 1:
			s += "|".center(tlen, " ")
		else:
			s += "/".center(len(c[0][0])) + " "
			if n == 3:
				s += "|".center(len(c[1][0])) + " "
			s += "\\".center(len(c[-1][0]))
		s += "\n"

		c = list(list(j for j in x if j.strip() != "") for x in c)
		max_lines = max(len(x) for x in c)
		for i, x in enumerate(c):
			clen = len(x[0])			
			while len(c[i]) < max_lines:
				c[i].append(" "*clen)

		for i in range(max_lines):
			s += " ".join(x[i] for x in c) + "\n"

		return s

	@staticmethod
	def from_leaves(branching_factors, leaves):
		assert len(leaves) == np.prod(branching_factors)
		trees = list(map(Tree, leaves))
		for b in branching_factors[::-1]:
			next_layer = []
			while len(trees) > 0:
				children = trees[:b]
				trees = trees[b:]
				next_layer.append(Tree(children=children))
			trees = next_layer
		assert len(trees) == 1
		return trees[0]


clipped = []
def minimax(root, is_max=True, α=-np.inf, β=np.inf):
	global clipped
	if root.value is not None:
		return root.value
	value = -np.inf if is_max else np.inf
	for i, c in enumerate(root.children):
		cmp = max if is_max else min 
		value = cmp(value, minimax(c, not is_max, α, β))
		if is_max:
			if value >= β:
				clipped += root.children[i+1:]
				return value
			if value < α:
				α = value
		else:
			if value <= α:
				clipped += root.children[i+1:]
				return value
			if value < β:
				β = value
	return value


tree = Tree.from_leaves([3,2,2,2], [1,-15,2,19,18,23,4,3,2,1,7,8,9,10,-2,5,-1,-30,4,7,20,-1,-1,-5])

print(tree)
print(minimax(tree))
for c in clipped:
	print(c, end="")



###################OUTPUT#################
#
#
#          /                   |                   \
#     /          \        /        \         /           \
#   /    \     /    \   /   \   /    \     /     \    /     \
# /  \  / \  /  \  / \ / \ / \ / \  /  \ /   \  / \ /  \  /  \
# 1 -15 2 19 18 23 4 3 2 1 7 8 9 10 -2 5 -1 -30 4 7 20 -1 -1 -5
#
# 7
#
# / \
# 4 3
#
# /  \
# -2 5