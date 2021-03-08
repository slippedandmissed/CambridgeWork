package uk.ac.cam.cl.jbs52.exercises;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Map;
import java.util.Set;
import java.util.Stack;

import uk.ac.cam.cl.mlrd.exercises.social_networks.IExercise11;

public class Exercise11 implements IExercise11 {

	private Map<Integer, Set<Integer>> loadGraph(Path graphFile) throws IOException {
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
	public Map<Integer, Double> getNodeBetweenness(Path graphFile) throws IOException {
		Map<Integer, Set<Integer>> graph = loadGraph(graphFile);

		Map<Integer, Double> centrality = new HashMap<Integer, Double>();
		for (int s : graph.keySet()) {
			centrality.put(s, 0.0);
		}
		
		LinkedList<Integer> Q = new LinkedList<Integer>();
		Stack<Integer> S = new Stack<Integer>();

		for (int s : graph.keySet()) {
			Map<Integer, Integer> sigma = new HashMap<Integer, Integer>();
			Map<Integer, Integer> dist = new HashMap<Integer, Integer>();
			Map<Integer, Set<Integer>> pred = new HashMap<Integer, Set<Integer>>();
			
			for (int v: graph.keySet()) {
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
						dist.put(w, dist.get(v)+1);
						Q.add(w);
					}
					
					if (dist.get(w) == dist.get(v)+1) {
						sigma.put(w, sigma.get(w)+sigma.get(v));
						pred.get(w).add(v);
					}

				}
			}

			Map<Integer, Double> delta = new HashMap<Integer, Double>();
			for (int v : graph.keySet()) {
				delta.put(v, 0.0);
			}

			while (!S.isEmpty()){
				int w = S.pop();
				
				for (int v : pred.get(w)) {
					delta.put(v, delta.get(v) + ((Double.valueOf(sigma.get(v)) / Double.valueOf(sigma.get(w))) * (1.0 + delta.get(w))));
				}
				if (w != s) {
					centrality.put(w, centrality.get(w) + delta.get(w)/2);
				}
			}
			
		}

		return centrality;
	}

}
