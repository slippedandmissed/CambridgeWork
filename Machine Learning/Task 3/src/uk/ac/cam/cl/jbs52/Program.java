package uk.ac.cam.cl.jbs52;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.TreeMap;
import java.util.function.Function;
import java.util.stream.Collectors;

import edu.stanford.nlp.ling.Word;
import edu.stanford.nlp.process.PTBTokenizer;
import edu.stanford.nlp.process.WordTokenFactory;
import uk.ac.cam.cl.mlrd.utils.ChartPlotter;
import uk.ac.cam.cl.mlrd.utils.BestFit;
import uk.ac.cam.cl.mlrd.utils.BestFit.Line;
import uk.ac.cam.cl.mlrd.utils.BestFit.Point;

public class Program {

	public static List<String> tokenize(Path textFile) throws IOException {
		List<String> result = new ArrayList<String>();
		try (BufferedReader reader = Files.newBufferedReader(textFile)) {
			PTBTokenizer<Word> tokenizer = new PTBTokenizer<Word>(reader, new WordTokenFactory(),
					"untokenizable=noneDelete");
			while (tokenizer.hasNext()) {
				String token = tokenizer.next().word().toLowerCase();
				result.add(token);
			}
		} catch (IOException e) {
			throw new IOException("Can't access file " + textFile, e);
		}
		return result;
	}
	
	public static Map<String, Long> countAllWords(String dir) throws IOException {
		return Files.list(Paths.get(dir)).map(arg0 -> {
			try {
				return tokenize(arg0);
			} catch (IOException e) {
				e.printStackTrace();
			}
			return null;
		}).flatMap(List::stream).collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
	}
	
	public static long uniqueWords(String dir, long n) throws IOException {
		return Files.list(Paths.get(dir)).map(arg0 -> {
			try {
				return tokenize(arg0);
			} catch (IOException e) {
				e.printStackTrace();
			}
			return null;
		}).flatMap(List::stream).limit(n).distinct().collect(Collectors.counting());

	}
	
	public static <A, B> Map<B, List<A>> rearrangeMap(Map<A, B> map) {
		return map.entrySet().stream().collect(
				Collectors.groupingBy(Map.Entry::getValue, Collectors.mapping(Map.Entry::getKey, Collectors.toList())));
	}

	private static class Pair<A, B> {
		public A a;
		public B b;

		public Pair(A a, B b) {
			this.a = a;
			this.b = b;
		}
	}

	public static <A, B> List<Pair<A, B>> flatten(Map<A, List<B>> map) {
		return map.entrySet().stream()
				.map(e -> (e.getValue().stream().map(f -> new Pair<A, B>(e.getKey(), f)).collect(Collectors.toList())))
				.flatMap(List::stream).collect(Collectors.toList());
	}


	public static void main(String[] args) throws IOException {
		String dataDir = "data/large_dataset";

		// Part 1
		Map<String, Long> frequencies = countAllWords(dataDir);
		List<Pair<Long, String>> sortedFrequencies = flatten(
				new TreeMap<Long, List<String>>(rearrangeMap(frequencies)));
		Collections.reverse(sortedFrequencies);

		// Part 2
		List<Point> points = new ArrayList<Point>();
		for (int i = 0; i < 10000; i++) {
			Pair<Long, String> p = sortedFrequencies.get(i);
			points.add(new Point(i + 1, p.a));
		}

		// Part 3
		List<String> markers = List.of("horrific", "satisfying", "exploiting", "awesome", "recommend", "unique",
				"incongruity", "pain", "escapist", "fun");

		List<Long> markerFrequencies = markers.stream().map(frequencies::get).collect(Collectors.toList());
		List<Point> markerPoints = new ArrayList<Point>();
		for (long f : markerFrequencies) {
			int min = 0;
			int max = sortedFrequencies.size() - 1;
			boolean found = false;
			while (!found) {
				if (max < min) {
					System.err.println("Oh no");
					break;
				}
				int i = (min + max) / 2;
				long v = sortedFrequencies.get(i).a;
				if (v == f) {
					found = true;
					markerPoints.add(new Point(i + 1, f));
				} else if (v > f) {
					min = i + 1;
				} else {
					max = i - 1;
				}
			}
		}
		// ChartPlotter.plotLines(points, markerPoints);

		// Part 4
		List<Point> logPoints = points.stream().map(e -> new Point(Math.log(e.x), Math.log(e.y)))
				.collect(Collectors.toList());

		// Part 5
		Map<Point, Double> weighted = logPoints.stream()
				.collect(Collectors.toMap(Function.identity(), e -> Math.exp(e.y)));
		Line bestFit = BestFit.leastSquares(weighted);
		List<Point> bestFitPoints = logPoints.stream()
				.map(e -> new Point(e.x, e.x * bestFit.gradient + bestFit.yIntercept)).collect(Collectors.toList());
		// ChartPlotter.plotLines(logPoints, bestFitPoints);
		
		// Part 6
		for (int i=0; i<markers.size(); i++) {
			String word = markers.get(i);
			Point a = markerPoints.get(i);
			double rank = a.x;
			double frequency = a.y;
			double predicted = Math.exp(Math.log(rank)*bestFit.gradient + bestFit.yIntercept);
			double error = predicted-frequency;
			double percentageError = error/frequency * 100;
			System.out.println(word);
			System.out.println(rank);
			System.out.println(frequency);
			System.out.println(predicted);
			System.out.println(error);
			System.out.println(""+percentageError+"%");
			System.out.println("");
		}
		
		// Part 7
		double k = Math.exp(bestFit.yIntercept);
		double alpha = -bestFit.gradient;
		System.out.println(k);
		System.out.println(alpha);
		
		// Step 2
		Map<Long, Long> tokensToTypes = new HashMap<Long, Long>();
		long tokenCount = frequencies.entrySet().stream().mapToLong(e->e.getValue()).sum();
		long tokens = 1;
		while (tokens < tokenCount) {
			tokensToTypes.put(tokens, uniqueWords(dataDir, tokens));
			tokens *= 2;
		}
		tokensToTypes.put(tokenCount, uniqueWords(dataDir, tokenCount));
		List<Point> heapLogs = tokensToTypes.entrySet().stream().map(e -> new Point(Math.log(e.getKey()), Math.log(e.getValue()))).collect(Collectors.toList());
		ChartPlotter.plotLines(heapLogs);
	}

}
