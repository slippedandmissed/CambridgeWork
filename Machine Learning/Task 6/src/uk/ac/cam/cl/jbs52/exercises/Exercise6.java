package uk.ac.cam.cl.jbs52.exercises;

import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.stream.Collectors;

import uk.ac.cam.cl.mlrd.exercises.sentiment_detection.IExercise6;
import uk.ac.cam.cl.mlrd.exercises.sentiment_detection.NuancedSentiment;
import uk.ac.cam.cl.mlrd.exercises.sentiment_detection.Sentiment;
import uk.ac.cam.cl.mlrd.exercises.sentiment_detection.Tokenizer;

public class Exercise6 implements IExercise6 {

	public Map<NuancedSentiment, Long> calculateClassCounts(Map<Path, NuancedSentiment> trainingSet)
			throws IOException {
		return trainingSet.values().stream().collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
	}

	@Override
	public Map<NuancedSentiment, Double> calculateClassProbabilities(Map<Path, NuancedSentiment> trainingSet)
			throws IOException {
		int size = trainingSet.size();
		return calculateClassCounts(trainingSet).entrySet().stream()
				.map(e -> Map.entry(e.getKey(), Double.valueOf(e.getValue()) / size))
				.collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));
	}

	private static <A, B> Map<B, List<A>> rearrangeMap(Map<A, B> map) {
		return map.entrySet().stream().collect(
				Collectors.groupingBy(Map.Entry::getValue, Collectors.mapping(Map.Entry::getKey, Collectors.toList())));
	}

	public Map<NuancedSentiment, Map<String, Long>> calculateTokenCounts(Map<Path, NuancedSentiment> trainingSet) {
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

	public Map<NuancedSentiment, Long> getTotalWordCounts(Map<Path, NuancedSentiment> trainingSet) {
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

	private Map<String, Map<NuancedSentiment, Double>> calculateLogProbs(Map<Path, NuancedSentiment> trainingSet,
			BiFunction<Double, Long, Double> formula) throws IOException {
		Map<NuancedSentiment, Long> totalWordCounts = getTotalWordCounts(trainingSet);
		Map<String, Map<NuancedSentiment, Double>> map = new HashMap<String, Map<NuancedSentiment, Double>>();

		Map<NuancedSentiment, Map<String, Long>> tokenCounts = calculateTokenCounts(trainingSet);
		Set<NuancedSentiment> classes = tokenCounts.keySet();

		for (NuancedSentiment s : classes) {
			Map<String, Long> occurances = tokenCounts.get(s);
			Long wc = totalWordCounts.get(s);
			Map<String, Map<NuancedSentiment, Double>> logProbs = new HashMap<>(
					occurances.entrySet().stream().collect(Collectors.toMap(Map.Entry::getKey,
							e -> Map.of(s, formula.apply(Double.valueOf(e.getValue()), wc)))));

			deepAppend(map, logProbs);

		}
		for (Map<NuancedSentiment, Double> inner : map.values()) {
			for (NuancedSentiment s : classes) {
				if (inner.get(s) == null) {
					inner.put(s, formula.apply(0.0, totalWordCounts.get(s)));
				}
			}
		}

		return map;
	}

	@Override
	public Map<String, Map<NuancedSentiment, Double>> calculateNuancedLogProbs(Map<Path, NuancedSentiment> trainingSet)
			throws IOException {
		long w = calculateTokenCounts(trainingSet).entrySet().stream().map(x -> x.getValue().keySet())
				.flatMap(Set::stream).collect(Collectors.toSet()).size();
		return calculateLogProbs(trainingSet, (v, wc) -> Math.log((v + 1) / (wc + w)));
	}

	@Override
	public Map<Path, NuancedSentiment> nuancedClassifier(Set<Path> testSet,
			Map<String, Map<NuancedSentiment, Double>> tokenLogProbs, Map<NuancedSentiment, Double> classProbabilities)
			throws IOException {
		Map<Path, NuancedSentiment> map = new HashMap<Path, NuancedSentiment>();

		for (Path path : testSet) {
			List<String> words = Tokenizer.tokenize(path);
			Map<NuancedSentiment, Double> p = new HashMap<NuancedSentiment, Double>();
			for (String word : words) {
				Map<NuancedSentiment, Double> logProbs = tokenLogProbs.get(word);
				if (logProbs != null) {
					for (Map.Entry<NuancedSentiment, Double> i : logProbs.entrySet()) {
						NuancedSentiment s = i.getKey();
						Double current = p.get(s);
						if (current == null) {
							current = 0.0;
						}
						current += i.getValue();
						p.put(s, current);
					}
				}
			}
			Map.Entry<NuancedSentiment, Double> max = null;
			for (Map.Entry<NuancedSentiment, Double> i : p.entrySet()) {
				if (max == null || i.getValue() > max.getValue()) {
					max = i;
				}
			}
			map.put(path, max.getKey());
		}

		return map;
	}

	@Override
	public double nuancedAccuracy(Map<Path, NuancedSentiment> trueSentiments,
			Map<Path, NuancedSentiment> predictedSentiments) {
		double correct = 0;
		for (Path path : trueSentiments.keySet()) {
			if (trueSentiments.get(path) == predictedSentiments.get(path)) {
				correct++;
			}
		}
		return correct / trueSentiments.size();
	}

	@Override
	public Map<Integer, Map<Sentiment, Integer>> agreementTable(
			Collection<Map<Integer, Sentiment>> predictedSentiments) {

		return predictedSentiments.stream().map(Map::entrySet).flatMap(Collection::stream)
				.collect(Collectors.groupingBy(e -> e.getKey(),
						Collectors.groupingBy(e -> e.getValue(), Collectors.reducing(0, e -> 1, Math::addExact))));
	}

	@Override
	public double kappa(Map<Integer, Map<Sentiment, Integer>> agreementTable) {
		
		int N = agreementTable.size();
		double Pe = 0;
		for (Sentiment j: Sentiment.values()) {
			double inner = 0;
			for (Integer i: agreementTable.keySet()) {
				Map<Sentiment, Integer> row = agreementTable.get(i);
				double ni = row.values().stream().mapToDouble(e -> e).sum();
				Integer nij = row.get(j);
				if (nij == null) {
					nij = 0;
				}
				inner += nij/ni;
			}
			inner = inner / N;
			Pe += inner * inner;
		}
		
		double Pa = 0;
		for (Integer i: agreementTable.keySet()) {
			Map<Sentiment, Integer> row = agreementTable.get(i);
			double inner = 0;
			for (Sentiment j: Sentiment.values()) {
				Integer nij = row.get(j);
				if (nij == null) {
					nij = 0;
				}
				inner += nij*(nij-1);
			}
			double ni = row.values().stream().mapToDouble(e -> e).sum();
			inner = inner / (ni*(ni-1));
			Pa += inner;
		}
		Pa = Pa/N;
				
		return (Pa-Pe)/(1-Pe);
	}

}
