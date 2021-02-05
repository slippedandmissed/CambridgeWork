package uk.ac.cam.cl.jbs52.exercises;

import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.stream.Collector;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import uk.ac.cam.cl.mlrd.exercises.sentiment_detection.IExercise2;
import uk.ac.cam.cl.mlrd.exercises.sentiment_detection.Sentiment;
import uk.ac.cam.cl.mlrd.exercises.sentiment_detection.Tokenizer;

public class Exercise2 implements IExercise2 {

	public Map<Sentiment, Long> calculateClassCounts(Map<Path, Sentiment> trainingSet) throws IOException {
		return trainingSet.values().stream().collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
	}

	@Override
	public Map<Sentiment, Double> calculateClassProbabilities(Map<Path, Sentiment> trainingSet) throws IOException {
		int size = trainingSet.size();
		return calculateClassCounts(trainingSet).entrySet().stream()
				.map(e -> Map.entry(e.getKey(), Double.valueOf(e.getValue()) / size))
				.collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));
	}

	private static <A, B> Map<B, List<A>> rearrangeMap(Map<A, B> map) {
		return map.entrySet().stream().collect(
				Collectors.groupingBy(Map.Entry::getValue, Collectors.mapping(Map.Entry::getKey, Collectors.toList())));
	}

	public Map<Sentiment, Map<String, Long>> calculateTokenCounts(Map<Path, Sentiment> trainingSet) {
		return rearrangeMap(trainingSet).entrySet().stream()
				.collect(Collectors.toMap(Map.Entry::getKey, e -> e.getValue().stream().map(f -> {
					try {
						return Tokenizer.tokenize(f);
					} catch (IOException e1) {
						e1.printStackTrace();
						return new ArrayList<String>();
					}
				}).flatMap(List::stream).collect(Collectors.groupingBy(Function.identity(), Collectors.counting()))));
	}

	public Map<Sentiment, Long> getTotalWordCounts(Map<Path, Sentiment> trainingSet) {
		return calculateTokenCounts(trainingSet).entrySet().stream().collect(
				Collectors.toMap(Map.Entry::getKey, e -> e.getValue().values().stream().mapToLong(x -> x).sum()));
	}

	private static <A, B, C> void deepAppend(Map<A, Map<B, C>> x, Map<A, Map<B, C>> y) {
		for (A a : y.keySet()) {
			Map<B, C> xInner = x.get(a);
			Map<B, C> yInner = y.get(a);
			if (xInner == null) {
				x.put(a, new HashMap<>(yInner));
			} else {
				for (B b : yInner.keySet()) {
					xInner.put(b, yInner.get(b));
				}
			}
		}
	}

	private Map<String, Map<Sentiment, Double>> calculateLogProbs(Map<Path, Sentiment> trainingSet,
			BiFunction<Double, Long, Double> formula) throws IOException {
		Map<Sentiment, Long> totalWordCounts = getTotalWordCounts(trainingSet);
		Map<String, Map<Sentiment, Double>> map = new HashMap<String, Map<Sentiment, Double>>();

		Map<Sentiment, Map<String, Long>> tokenCounts = calculateTokenCounts(trainingSet);
		Set<Sentiment> classes = tokenCounts.keySet();

		for (Sentiment s : classes) {
			Map<String, Long> occurances = tokenCounts.get(s);
			Long wc = totalWordCounts.get(s);
			Map<String, Map<Sentiment, Double>> logProbs = new HashMap<>(
					occurances.entrySet().stream().collect(Collectors.toMap(Map.Entry::getKey,
							e -> Map.of(s, formula.apply(Double.valueOf(e.getValue()), wc)))));

			deepAppend(map, logProbs);

		}
		for (Map<Sentiment, Double> inner : map.values()) {
			for (Sentiment s : classes) {
				if (inner.get(s) == null) {
					inner.put(s, formula.apply(0.0, totalWordCounts.get(s)));
				}
			}
		}

		return map;
	}

	@Override
	public Map<String, Map<Sentiment, Double>> calculateUnsmoothedLogProbs(Map<Path, Sentiment> trainingSet)
			throws IOException {
		return calculateLogProbs(trainingSet, (v, wc) -> Math.log(v / wc));
	}

	@Override
	public Map<String, Map<Sentiment, Double>> calculateSmoothedLogProbs(Map<Path, Sentiment> trainingSet)
			throws IOException {
		long w = calculateTokenCounts(trainingSet).entrySet().stream().map(x -> x.getValue().keySet())
				.flatMap(Set::stream).collect(Collectors.toSet()).size();
		return calculateLogProbs(trainingSet, (v, wc) -> Math.log((v + 1) / (wc + w)));
	}

	@Override
	public Map<Path, Sentiment> naiveBayes(Set<Path> testSet, Map<String, Map<Sentiment, Double>> tokenLogProbs,
			Map<Sentiment, Double> classProbabilities) throws IOException {
		Map<Path, Sentiment> map = new HashMap<Path, Sentiment>();

		for (Path path : testSet) {
			List<String> words = Tokenizer.tokenize(path);
			Map<Sentiment, Double> p = new HashMap<Sentiment, Double>();
			for (String word : words) {
				Map<Sentiment, Double> logProbs = tokenLogProbs.get(word);
				if (logProbs != null) {
					for (Map.Entry<Sentiment, Double> i : logProbs.entrySet()) {
						Sentiment s = i.getKey();
						Double current = p.get(s);
						if (current == null) {
							current = 0.0;
						}
						current += i.getValue();
						p.put(s, current);
					}
				}
			}
			Map.Entry<Sentiment, Double> max = null;
			for (Map.Entry<Sentiment, Double> i : p.entrySet()) {
				if (max == null || i.getValue() > max.getValue()) {
					max = i;
				}
			}
			map.put(path, max.getKey());
		}

		return map;
	}

}
