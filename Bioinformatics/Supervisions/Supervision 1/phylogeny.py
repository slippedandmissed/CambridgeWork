#!/usr/bin/python3.9

from pptree import print_tree
from copy import deepcopy
from io import StringIO
import numpy as np
import sys

real_stdout = sys.stdout

class Node:
    def __init__(self, name, parent=None, parent_distance=None):
        self.name = name
        self.parent = parent
        self.parent_distance = parent_distance
        self.children = {}
        self.intermediate_name_ctr = 0
    
    def __str__(self):
        sys.stdout = my_stdout = StringIO()
        print_tree(self, childattr="children_list", nameattr="name_with_parent_distance", horizontal=False)
        s = my_stdout.getvalue()
        sys.stdout = real_stdout
        return s
    
    def __repr__(self):
        return self.name

    @property
    def name_with_parent_distance(self):
        return self.name if self.parent_distance is None else f"{self.parent_distance}: {self.name}"

    @property
    def children_list(self):
        return list(x for _, x in self.children.values())
    
    def get_new_intermediate_name(self):
        self.intermediate_name_ctr += 1
        return f"{self.name}.{self.intermediate_name_ctr}"
    
    def add_child(self, name, length):
        child = Node(name, parent=self, parent_distance=length)
        self.children[name] = (length, child)
        return child
    
    def get_descendant(self, name):
        if self.name == name:
            return self, []
        for child_name, child in self.children.items():
            desc, desc_path = child[1].get_descendant(name)
            if desc is not None:
                return desc, [child[1]] + desc_path
        return None, None
    
    def insert_between(self, i, j, distance_from_i):
        i_node, _ = self.get_descendant(i)
        assert i_node is not None, f"Tree {self.name} does not contain node {i}"
        cumulative_distance = 0
        current = i_node
        desc_path = None
        while current.name != j:
            assert current is not None, f"Tree {self.name} does not contain node {j}"

            if desc_path is None:
                _, desc_path = current.get_descendant(j)
            
            if desc_path is None:
                assert current.parent is not None, f"Tree {self.name} does not contain node {j}"

            if cumulative_distance == distance_from_i:
                return current.name

            if desc_path is None:
                nxt = current.parent
                dst_to_nxt = current.parent_distance
                parent_of_intermediate = current.parent
                child_of_intermediate = current
            else:
                nxt = desc_path[0]
                desc_path = desc_path[1:]
                dst_to_nxt = nxt.parent_distance
                parent_of_intermediate = current
                child_of_intermediate = nxt
            
            new_cumulative_distance = cumulative_distance + dst_to_nxt
            if new_cumulative_distance > distance_from_i:
                overshoot = new_cumulative_distance - distance_from_i
                
                upper_length = overshoot if desc_path is None else dst_to_nxt - overshoot
                
                intermediate = parent_of_intermediate.add_child(parent_of_intermediate.get_new_intermediate_name(), upper_length)
                del parent_of_intermediate.children[child_of_intermediate.name]
                intermediate.children[child_of_intermediate.name] = (dst_to_nxt - upper_length, child_of_intermediate)
                child_of_intermediate.parent = intermediate
                child_of_intermediate.parent_distance -= upper_length
                return intermediate.name

            cumulative_distance = new_cumulative_distance
            current = nxt

        assert False, f"Total distance between {i} and {j} is {cumulative_distance}, which is less than split distance {distance_from_i}"

    def connect_to(self, i, new_node_name, length):
        i_node, _ = self.get_descendant(i)
        assert i_node is not None, f"Tree {self.name} does not contain node {i}"
        i_node.add_child(new_node_name, length)
        
    def distance_between(self, i, j):
        i_node, i_path = self.get_descendant(i)
        assert i_node is not None, f"Tree {self.name} does not contain node {i}"
        j_node, j_path = self.get_descendant(j)
        assert j_node is not None, f"Tree {self.name} does not contain node {j}"
        idx = 0
        for idx, x in enumerate(i_path):
            if (idx >= len(j_path)):
                break
            y = j_path[idx]
            if x.name != y.name:
                break
        else:
            if idx == len(j_path)-1:
                return 0
        return sum(n.parent_distance for n in (i_path[idx:] + j_path[idx:]) if n.parent is not None)

    def add_existing_node_as_child(self, child, distance):
        assert child.parent is None, f"Cannot add node {child.name} as child, as it already has a parent: {child.parent.name}"
        self.children[child.name] = (distance, child)
        child.parent = self
        child.parent_distance = distance

    def match_against(self, D):
        for i, x in D.items():
            for j, d in x.items():
                r = self.distance_between(i, j)
                assert d == r, f"Distance between {i} and {j} is {r}, when it is supposed to be {d}"

def additive_phylogeny(D):
    def limb_length(x, D):
        keys = list(D.keys())
        i = keys.index(x)
        N = len(keys)
        L = np.empty((N, N))
        L[:,:] = np.inf
        for j, y in enumerate(keys):
            if j == i:
                continue
            for k, z in enumerate(keys):
                if k == i or k == j:
                    continue

                L[k][j] = (D[x][z] + D[y][x] - D[y][z])/2

        idx = np.argmin(L)
        j, k = idx // N, idx % N
        return np.min(L), keys[j], keys[k]

    keys = list(D.keys())
    num_keys = len(keys)
    if num_keys == 0:
        return None
    elif num_keys == 1:
        return Node(keys[0])
    elif num_keys == 2:
        tree = Node(keys[0])
        tree.add_child(keys[1], D[keys[0]][keys[1]])
        return tree

    j = keys[0]
    l, *_ = limb_length(j, D)
    D_bald = deepcopy(D)
    for key in keys:
        if key == j:
            continue
        D_bald[key][j] -= l
        D_bald[j][key] -= l
    
    D_trim = deepcopy(D_bald)
    del D_trim[j]
    for key in keys:
        if key == j:
            continue
        del D_trim[key][j]

    tree = additive_phylogeny(D_trim)

    _, i, k = limb_length(j, D_bald)

    n = tree.insert_between(i, k, D_bald[i][j])
    tree.connect_to(n, j, l)

    return tree

class Cluster(Node):
    def __init__(self, name, age):
        super().__init__(name)
        self.age = age

def upgma(D):
    if (len(D.keys()) == 0):
        return None

    def get_leaves(tree):
        result = [tree.name] if  "{" not in tree.name and "." not in tree.name else []
        for _, i in tree.children.values():
            result += get_leaves(i)
        return result

    D = deepcopy(D)
    clusters = []
    for i in D.keys():
        clusters.append(Cluster(i, 0))

    while len(clusters) > 1:
        davg = {}
        min_davg = None
        min_davg_clusters = None
        for c1 in clusters:
            davg[c1.name] = {}
            for c2 in clusters:
                if c2 == c1:
                    continue

                davg[c1.name][c2.name] = 0
                c1_leaves = get_leaves(c1)
                c2_leaves = get_leaves(c2)
                for i in c1_leaves:
                    for j in c2_leaves:
                        davg[c1.name][c2.name] += D[i][j]
                davg[c1.name][c2.name] /= (len(c1_leaves) * len(c2_leaves))
                
                if min_davg is None or min_davg > davg[c1.name][c2.name]:
                    min_davg = davg[c1.name][c2.name]
                    min_davg_clusters = (c1, c2)

        age = min_davg/2
        new_cluster = Cluster(f"{{{','.join(x.name for x in min_davg_clusters)}}}", age)
        new_cluster.add_existing_node_as_child(min_davg_clusters[0], age - min_davg_clusters[0].age)
        new_cluster.add_existing_node_as_child(min_davg_clusters[1], age - min_davg_clusters[1].age)
        clusters = list(c for c in clusters if c not in min_davg_clusters)
        clusters.append(new_cluster)
        
        for c in D.values():
            c[new_cluster.name] = (c[min_davg_clusters[0].name]+c[min_davg_clusters[1].name])/2
        
        D[new_cluster.name] = {}
        for c in D:
            if c == new_cluster.name:
                continue
            D[new_cluster.name][c] = D[c][new_cluster.name]        

        D[new_cluster.name][new_cluster.name] = 0

    return clusters[0]


def neighbor_joining(D, new_node_ctr=0):
    def total_distance(i):
        total = 0
        for j, d in D[i].items():
            if j == i:
                continue
            total += d
        return total
    
    keys = list(D.keys())
    num_keys = len(keys)
    if num_keys == 0:
        return None
    elif num_keys == 1:
        return Node(keys[0])
    elif num_keys == 2:
        tree = Node(keys[0])
        tree.add_child(keys[1], D[keys[0]][keys[1]])
        return tree
    
    D = deepcopy(D)
    n = len(list(D.keys()))
    D_ = {}
    min_dst = None
    min_dst_idxs = None
    for i, row in D.items():
        D_[i] = {}
        for j, d in row.items():
            if i == j:
                D_[i][j] = 0
            else:
                dst = (n-2)*D[i][j] - total_distance(i) - total_distance(j)
                D_[i][j] = dst
                if min_dst is None or min_dst > dst:
                    min_dst = dst
                    min_dst_idxs = (i, j)
    
    i, j = min_dst_idxs
    Δ = (total_distance(i) - total_distance(j)) / (n-2)
    limb_length_i = (D[i][j] + Δ) / 2
    limb_length_j = (D[i][j] - Δ) / 2

    D__ = deepcopy(D)
    del D__[i]
    del D__[j]
    for c in D__.values():
        del c[i]
        del c[j]
    
    m = f"m.{new_node_ctr}"
    D__[m] = {}
    for k in D__:
        d_km = 0 if k == m else (D[i][k] + D[j][k] - D[i][j])/2
        D__[m][k] = d_km
        D__[k][m] = d_km
    
    tree = neighbor_joining(D__, new_node_ctr=new_node_ctr+1)
    
    tree.connect_to(m, i, limb_length_i)
    tree.connect_to(m, j, limb_length_j)

    return tree

# D = {
#     "i": {"i": 0, "j": 13, "k": 21, "l": 22},
#     "j": {"i": 13, "j": 0, "k": 12, "l": 13},
#     "k": {"i": 21, "j": 12, "k": 0, "l": 13},
#     "l": {"i": 22, "j": 13, "k": 13, "l": 0}
# }

D = {
    "A": {"A": 0, "B": 6, "C": 9, "D": 14},
    "B": {"A": 6, "B": 0, "C": 5, "D": 10},
    "C": {"A": 9, "B": 5, "C": 0, "D": 9},
    "D": {"A": 14, "B": 10, "C": 9, "D": 0}
}

# D = {
#     "i": {"i": 0, "j": 3, "k": 4, "l": 3},
#     "j": {"i": 3, "j": 0, "k": 4, "l": 5},
#     "k": {"i": 4, "j": 4, "k": 0, "l": 2},
#     "l": {"i": 3, "j": 5, "k": 2, "l": 0}
# }


# x = additive_phylogeny(D)
# x = upgma(D)
# x = neighbor_joining(D)
# print(x)
# x.match_against(D)

print(additive_phylogeny(D))
print(upgma(D))
print(neighbor_joining(D))