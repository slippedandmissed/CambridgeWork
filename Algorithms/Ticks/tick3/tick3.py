#!/usr/bin/python3.9

def bfs(graph, vertices, source):
    frontier = [source]
    reachable = {}
    come_from = {}
    for v in vertices:
        reachable[v] = False
        come_from[v] = None

    while len(frontier):
        u = frontier[0]
        frontier = frontier[1:]
        reachable[u] = True
        if u in graph:
            for v in graph[u]:
                if come_from[v] is None:
                    come_from[v] = u
                    frontier.append(v)

    return reachable, come_from


def compute_max_flow(capacity, source, sink):
    flow = {e: 0 for e in capacity}

    def find_augmenting_path():
        aug = {}
        for (u, v), c in capacity.items():
            if flow[(u, v)] < c:
                aug[(u, v)] = (0, c-flow[(u, v)])
            if flow[(u, v)] > 0:
                aug[(v, u)] = (1, flow[(u, v)])

        graph = {}
        vertices = []
        for (u, v) in aug:
            if u not in vertices:
                vertices.append(u)
            if v not in vertices:
                vertices.append(v)
            if u not in graph:
                graph[u] = []
            if v not in graph[u]:
                graph[u].append(v)

        reachable, come_from = bfs(graph, vertices, source)
        if reachable[sink]:
            path = []
            current = sink
            delta = None
            while (current != source):
                prev = come_from[current]
                e, d = aug[(prev, current)]
                if delta is None or d < delta:
                    delta = d
                path = [(prev, current, e)]+path
                current = prev
            return path, delta if delta is not None else 0
        else:
            return None, reachable

    reachable = None
    while True:
        p, delta = find_augmenting_path()
        if p is None:
            reachable = delta
            break
        else:
            for (prev, current, e) in p:
                if e == 0:
                    flow[(prev, current)] += delta
                else:
                    flow[(current, prev)] -= delta

    t = 0
    for (u, v), c in flow.items():
        if u == source:
            t += c
        if v == source:
            t -= c

    return t, flow, set(i for i in reachable if reachable[i])
