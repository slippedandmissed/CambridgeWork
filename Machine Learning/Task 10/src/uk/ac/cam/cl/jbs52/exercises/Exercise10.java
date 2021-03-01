package uk.ac.cam.cl.jbs52.exercises;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import uk.ac.cam.cl.mlrd.exercises.social_networks.IExercise10;

public class Exercise10 implements IExercise10 {

	@Override
	public Map<Integer, Set<Integer>> loadGraph(Path graphFile) throws IOException {
		BufferedReader reader = Files.newBufferedReader(graphFile, Charset.forName("UTF-8"));
		String currentLine;
		Map<Integer, Set<Integer>> map = new HashMap<Integer, Set<Integer>>();
		while ((currentLine = reader.readLine()) != null) {
			String[] parts = currentLine.split(" ");
			int i = Integer.parseInt(parts[0]);
			int j = Integer.parseInt(parts[1]);
			Set<Integer> set1 = map.get(i);
			if (set1 == null) {
				set1 = new HashSet<Integer>();
				map.put(i, set1);
			}
			set1.add(j);

			Set<Integer> set2 = map.get(j);
			if (set2 == null) {
				set2 = new HashSet<Integer>();
				map.put(j, set2);
			}
			set2.add(i);
		}
		return map;
	}

	@Override
	public Map<Integer, Integer> getConnectivities(Map<Integer, Set<Integer>> graph) {
		return graph.entrySet().stream().collect(Collectors.toMap(Map.Entry::getKey, e -> e.getValue().size()));
	}
		
	private static class Pair {
		int node;
		int dst;

		public Pair(int node, int dst) {
			this.node = node;
			this.dst = dst;
		}
	}


	private Map<Integer, Integer> shortestPath(Map<Integer, Set<Integer>> graph, int start) {

		Map<Integer, Integer> visited = new HashMap<Integer, Integer>();
		LinkedList<Pair> frontier = new LinkedList<Pair>();

		frontier.add(new Pair(start, 0));

		Pair current;
		while (!frontier.isEmpty()) {
			current = frontier.remove();
			int node = current.node;
			int dst = current.dst;
			Set<Integer> neighbours = graph.get(node);
			for (int connected : neighbours) {
				if (visited.get(connected) == null) {
					visited.put(connected, dst + 1);
					frontier.add(new Pair(connected, dst + 1));
				}
			}
		}
		return visited;
	}

	@Override
	public int getDiameter(Map<Integer, Set<Integer>> graph) {
		int maxDiameter = 0;
		int i = 0;
		for (int a : graph.keySet()) {
			System.out.println(""+i+++"/"+graph.size());
			int dst = shortestPath(graph, a).values().stream().mapToInt(Integer::intValue).max().orElse(0);
			if (dst > maxDiameter) {
				maxDiameter = dst;
			}
			System.out.println(dst);
		}

		return maxDiameter;
	}

}
