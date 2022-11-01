# Algorithm Descriptions[^1]

[^1]: https://stemlounge.com/animated-algorithms-for-the-traveling-salesman-problem/

## Greedy Algorithm

In this example, all possible edges are sorted by distance, shortest to longest. Then the shortest edge that will neither create a vertex with more than 2 edges, nor a cycle with less than the total number of cities is added. This is repeated until we have a cycle containing all of the cities.

## Nearest Neighbor

The nearest neighbor heuristic is another greedy algorithm, or what some may call naive. It starts at one city and connects with the closest unvisited city. It repeats until every city has been visited. It then returns to the starting city.

## Nearest Insertion

One implementation of Nearest Insertion begins with two cities. It then repeatedly finds the city not already in the tour that is closest to any city in the tour, and places it between whichever two cities would cause the resulting tour to be the shortest possible. It stops when no more insertions remain.

## Cheapest Insertion

Like Nearest Insertion, Cheapest Insertion also begins with two cities. It then finds the city not already in the tour that when placed between two connected cities in the subtour will result in the shortest possible tour. It inserts the city between the two connected cities, and repeats until there are no more insertions left.

## Random Insertion

Random Insertion also begins with two cities. It then randomly selects a city not already in the tour and inserts it between two cities in the tour. Rinse, wash, repeat.

## Farthest Insertion

It then repeatedly finds the city not already in the tour that is furthest from any city in the tour, and places it between whichever two cities would cause the resulting tour to be the shortest possible.

## Christofides Algorithm

Christofides algorithm is a heuristic with a 3/2 approximation guarantee. In the worst case the tour is no longer than 3/2 the length of the optimum tour.

Due to its speed and 3/2 approximation guarantee, Christofides algorithm is often used to construct an upper bound, as an initial tour which will be further optimized using tour improvement heuristics, or as an upper bound to help limit the search space for branch and cut techniques used in search of the optimal route.

For it to work, it requires distances between cities to be symmetric and obey the triangle inequality, which is what you'll find in a typical x,y coordinate plane (metric space). Published in 1976, it continues to hold the record for the best approximation ratio for metric space.

## 2-Opt

2-Opt is a local search tour improvement algorithm proposed by Croes in 1958. It originates from the idea that tours with edges that cross over aren’t optimal. 2-opt will consider every possible 2-edge swap, swapping 2 edges when it results in an improved tour.

## 3-opt

3-opt is a generalization of 2-opt, where 3 edges are swapped at a time. When 3 edges are removed, there are 7 different ways of reconnecting them, so they're all considered.

## Lin-Kernighan Heuristic

Lin-Kernighan is an optimized k-Opt tour-improvement heuristic. It takes a tour and tries to improve it.

By allowing some of the intermediate tours to be more costly than the initial tour, Lin-Kernighan can go well beyond the point where a simple 2-Opt would terminate.

## Slime Mold Algorithm

[Slime Mold Algorithm](https://www.sciencedirect.com/science/article/pii/S0167739X19320941)

## Ant Colony Optimization

[Ant Colony Optimization](http://www.cs.unibo.it/babaoglu/courses/cas05-06/tutorials/Ant_Colony_Optimization.pdf)

# Comparison

| **Algorithm** | **Time Complexity** | **Could be Generalised** | **Generalization Notes** | **Category** |
|---|---|---|---|---|
| Nearest Neighbor | $\mathcal{O}(n^2)$ | Yes | Take a step of size $\delta x$ in the direction of lowest cost (including near miss tax) | Head-first |
| Nearest Insertion | $\mathcal{O}(n^2)$ | Yes | Somehow stretch existing contour to get closer to inserted city | Insertion |
| Cheapest Insertion | $\mathcal{O}(n^2\log{n})$ | Yes | Somehow stretch existing contour to get closer to inserted city | Insertion |
| Random Insertion | $\mathcal{O}(n^2)$ | Yes | Somehow stretch existing contour to get closer to inserted city | Insertion |
| Farthest Insertion | $\mathcal{O}(n^2)$ | Yes | Somehow stretch existing contour to get closer to inserted city | Insertion |
| Christofides Algorithm | $\mathcal{O}(n^4)$ | Not sure but would be amazing | Would require a "minimum spanning contour" of sorts. | Misc. |
| 2-opt | $\mathcal{O}(n^2)$ | Yes | Would require a notion of "swapping edge contours" | Optimization |
| 3-opt | $\mathcal{O}(n^3)$ | Yes | Would require a notion of "swapping edge contours" | Optimization |
| Lin-Kernighan Heuristic |  | Possibly | Would require a notion of "swapping edge contours" | Optimization |
| Slime Mold Algorithm |  | Yes | Slimes would be able to grow through the continuum | Head-first |
| Ant Colony Optimization | $\mathcal{O}(n^3)$ | Yes | Ants would be able to move through the continuum | Head-first |