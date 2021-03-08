package uk.ac.cam.cl.jbs52.exercises;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Stack;

import uk.ac.cam.cl.mlrd.exercises.social_networks.IExercise12;

public class Exercise12 implements IExercise12 {

	private int fuzzyCompare(double a, double b) {
		double t = 1e-06;
		if (a > b+t) {
			return 1;
		}
		if (a < b-t) {
			return -1;
		}
		return 0;
	}

	@Override
	public List<Set<Integer>> GirvanNewman(Map<Integer, Set<Integer>> graph, int minimumComponents) {
		List<Set<Integer>> components = getComponents(graph);
		while (components.size() < minimumComponents) {
			Map<Integer, Map<Integer, Double>> betweenness = getEdgeBetweenness(graph);
			double maxBetweenness = -1.0;
			for (int u : betweenness.keySet()) {
				for (int v : betweenness.get(u).keySet()) {
					double b = betweenness.get(u).get(v);
					if (fuzzyCompare(b, maxBetweenness) > 0) {
						maxBetweenness = b;
					}
				}
			}
			for (int u : betweenness.keySet()) {
				for (int v : betweenness.get(u).keySet()) {
					double b = betweenness.get(u).get(v);
					if (fuzzyCompare(b, maxBetweenness) == 0) {
						graph.get(u).remove(v);
					}
				}
			}
			components = getComponents(graph);
		}

		return components;
	}

	@Override
	public int getNumberOfEdges(Map<Integer, Set<Integer>> graph) {
		return (int) graph.values().stream().mapToInt(x -> x.size()).sum() / 2;
	}

	private void dfs(Map<Integer, Set<Integer>> graph, Map<Integer, Boolean> seen, List<Set<Integer>> clusterToVertex,
			int clusterCount, int start) {
		seen.put(start, true);
		clusterToVertex.get(clusterCount).add(start);
		for (int v : graph.get(start)) {
			if (!seen.get(v)) {
				dfs(graph, seen, clusterToVertex, clusterCount, v);
			}
		}
	}

	@Override
	public List<Set<Integer>> getComponents(Map<Integer, Set<Integer>> graph) {
		Set<Integer> vertices = graph.keySet();
		Map<Integer, Boolean> seen = new HashMap<Integer, Boolean>();
		for (int v : vertices) {
			seen.put(v, false);
		}
		List<Set<Integer>> clusterToVertex = new ArrayList<Set<Integer>>();

		int clusterCount = 0;

		for (int u : vertices) {
			if (!seen.get(u)) {
				clusterToVertex.add(new HashSet<Integer>());
				dfs(graph, seen, clusterToVertex, clusterCount++, u);
			}
		}
		return clusterToVertex;

	}

	@Override
	public Map<Integer, Map<Integer, Double>> getEdgeBetweenness(Map<Integer, Set<Integer>> graph) {
		Map<Integer, Map<Integer, Double>> centrality = new HashMap<Integer, Map<Integer, Double>>();
		for (Map.Entry<Integer, Set<Integer>> e : graph.entrySet()) {
			int u = e.getKey();
			Map<Integer, Double> c = centrality.get(u);
			if (c == null) {
				c = new HashMap<Integer, Double>();
				centrality.put(u, c);
			}
			for (int v : e.getValue()) {
				c.put(v, 0.0);
			}
		}

		LinkedList<Integer> Q = new LinkedList<Integer>();
		Stack<Integer> S = new Stack<Integer>();

		for (int s : graph.keySet()) {
			Map<Integer, Integer> sigma = new HashMap<Integer, Integer>();
			Map<Integer, Integer> dist = new HashMap<Integer, Integer>();
			Map<Integer, Set<Integer>> pred = new HashMap<Integer, Set<Integer>>();

			for (int v : graph.keySet()) {
				pred.put(v, new HashSet<>());
				dist.put(v, -1);
				sigma.put(v, 0);
			}

			dist.put(s, 0);
			sigma.put(s, 1);

			Q.add(s);

			while (!Q.isEmpty()) {
				int v = Q.remove();
				S.push(v);

				for (int w : graph.get(v)) {

					if (dist.get(w) == -1) {
						dist.put(w, dist.get(v) + 1);
						Q.add(w);
					}

					if (dist.get(w) == dist.get(v) + 1) {
						sigma.put(w, sigma.get(w) + sigma.get(v));
						pred.get(w).add(v);
					}

				}
			}

			Map<Integer, Double> delta = new HashMap<Integer, Double>();
			for (int v : graph.keySet()) {
				delta.put(v, 0.0);
			}

			while (!S.isEmpty()) {
				int w = S.pop();

				for (int v : pred.get(w)) {
					double c = (Double.valueOf(sigma.get(v)) / Double.valueOf(sigma.get(w))) * (1.0 + delta.get(w));
					centrality.get(v).put(w, centrality.get(v).get(w) + c);
					delta.put(v, delta.get(v) + c);
				}
			}

		}

		return centrality;
	}

}
