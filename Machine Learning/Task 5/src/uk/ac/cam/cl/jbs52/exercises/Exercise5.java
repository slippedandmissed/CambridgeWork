package uk.ac.cam.cl.jbs52.exercises;

import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.Random;
import java.util.function.Function;

import uk.ac.cam.cl.mlrd.exercises.sentiment_detection.IExercise1;
import uk.ac.cam.cl.mlrd.exercises.sentiment_detection.IExercise2;
import uk.ac.cam.cl.mlrd.exercises.sentiment_detection.IExercise5;
import uk.ac.cam.cl.mlrd.exercises.sentiment_detection.Sentiment;

public class Exercise5 implements IExercise5 {

	public final int FOLD_COUNT = 10;
	private final IExercise1 implementation1;
	private final IExercise2 implementation2;
	
	public Exercise5 () {
		implementation1 = new Exercise1();
		implementation2 = new Exercise2();
	}

	private <A> void shuffle(Random rng, List<A> list) {
		for (int i = 0; i < list.size(); i++) {
			int index = rng.nextInt(list.size());
			A tmp = list.get(index);
			list.set(index, list.get(i));
			list.set(i, tmp);
		}
	}

	@Override
	public List<Map<Path, Sentiment>> splitCVRandom(Map<Path, Sentiment> dataSet, int seed) {
		List<Map.Entry<Path, Sentiment>> entries = new ArrayList<Map.Entry<Path, Sentiment>>(dataSet.entrySet());
		shuffle(new Random(seed), entries);
		int maxFoldSize = (int) Math.ceil(entries.size() / FOLD_COUNT);

		int currentFoldSize = 0;
		Map<Path, Sentiment> currentFold = null;
		List<Map<Path, Sentiment>> folds = new ArrayList<Map<Path, Sentiment>>();

		for (int i = 0; i < entries.size(); i++) {
			if (currentFold == null || currentFoldSize >= maxFoldSize) {
				currentFold = new HashMap<Path, Sentiment>();
				folds.add(currentFold);
				currentFoldSize = 0;
			}
			Map.Entry<Path, Sentiment> entry = entries.get(i);
			currentFold.put(entry.getKey(), entry.getValue());
			currentFoldSize++;
		}

		return folds;
	}

	private static <A, B> Map<B, List<A>> rearrangeMap(Map<A, B> map) {
		return map.entrySet().stream().collect(
				Collectors.groupingBy(Map.Entry::getValue, Collectors.mapping(Map.Entry::getKey, Collectors.toList())));
	}

	private static <A> Map<A, Integer> roundRandomly(Random rng, Map<A, Double> map, int max) {
		List<A> keys = new ArrayList<A>(map.keySet());
		Map<A, Double> endPoints = new HashMap<A, Double>();
		for (int i = 0; i < map.size(); i++) {
			double prev;
			if (i == 0) {
				prev = 0;
			} else {
				prev = endPoints.get(keys.get(i - 1));
			}
			endPoints.put(keys.get(i), map.get(keys.get(i)) + prev);
		}
		Map<A, Integer> rounded = new HashMap<A, Integer>();
		for (A a : keys) {
			double endPoint = endPoints.get(a) % 1;
			double r = rng.nextDouble();
			int roundedEndPoint = Math.max(0,
					Math.min(max, (int) (r < endPoint ? Math.floor(endPoints.get(a)) : Math.ceil(endPoints.get(a)))));
			rounded.put(a, roundedEndPoint);
		}
		Map<A, Integer> diffs = new HashMap<A, Integer>();
		for (int i = 0; i < keys.size(); i++) {
			int prev;
			if (i == 0) {
				prev = 0;
			} else {
				prev = rounded.get(keys.get(i - 1));
			}
			diffs.put(keys.get(i), rounded.get(keys.get(i)) - prev);
		}
		return diffs;
	}

	private static <A> Map<A, Double> redistribute(Map<A, Double> desired, Map<A, Integer> available) {
		Map<A, Double> result = new HashMap<A, Double>();
		double defecit = 0;
		Map<A, Boolean> saturated = new HashMap<A, Boolean>();
		int saturatedCount = 0;
		for (Map.Entry<A, Double> e : desired.entrySet()) {
			A key = e.getKey();
			double value = e.getValue();
			int availableValue = available.get(key);
			if (value >= availableValue) {
				saturated.put(key, true);
				saturatedCount++;
				defecit += value - availableValue;
			} else {
				saturated.put(key, false);
			}
		}

		if (saturatedCount == desired.size()) {
			return available.entrySet().stream()
					.collect(Collectors.toMap(Map.Entry::getKey, e -> (double) e.getValue()));
		} else {
			double sharedDefecit = defecit / (desired.size() - saturatedCount);
			boolean overflow = false;
			for (Map.Entry<A, Boolean> e : saturated.entrySet()) {
				A key = e.getKey();
				boolean s = e.getValue();
				if (s) {
					result.put(key, (double) available.get(key));
				} else {
					double newVal = desired.get(key) + sharedDefecit;
					result.put(key, newVal);
					if (newVal > available.get(key)) {
						overflow = true;
					}
				}
			}
			if (overflow) {
				return redistribute(result, available);
			} else {
				return result;
			}
		}
	}

	@Override
	public List<Map<Path, Sentiment>> splitCVStratifiedRandom(Map<Path, Sentiment> dataSet, int seed) {
		int total = dataSet.size();
		Map<Sentiment, List<Path>> rearranged = rearrangeMap(dataSet);
		Map<Sentiment, Double> frequencies = rearranged.entrySet().stream()
				.collect(Collectors.toMap(Map.Entry::getKey, e -> ((double) e.getValue().size() / total)));
		Random rng = new Random(seed);
		for (List<Path> paths : rearranged.values()) {
			shuffle(rng, paths);
		}

		Map<Sentiment, Integer> remaining = rearranged.entrySet().stream()
				.collect(Collectors.toMap(Map.Entry::getKey, e -> ((int) e.getValue().size())));

		List<Map<Path, Sentiment>> folds = new ArrayList<Map<Path, Sentiment>>();
		int maxFoldSize = (int) Math.ceil(total / FOLD_COUNT);
		Map<Sentiment, Double> itemsToTake = frequencies.entrySet().stream()
				.collect(Collectors.toMap(Map.Entry::getKey, e -> ((double) e.getValue() * maxFoldSize)));

		
		List<Sentiment> sentiments = new ArrayList<Sentiment>(itemsToTake.keySet());
		shuffle(rng, sentiments);
		
		Map<Sentiment, Integer> startIndex = sentiments.stream().collect(Collectors.toMap(Function.identity(), e -> 0));

		for (int i = 0; i < FOLD_COUNT; i++) {
			Map<Path, Sentiment> currentFold = new HashMap<Path, Sentiment>();
			Map<Sentiment, Integer> roundedItemsToTake = roundRandomly(rng, redistribute(itemsToTake, remaining),
					maxFoldSize);
			for (Sentiment s: sentiments) {
				int start = startIndex.get(s);
				List<Path> paths = rearranged.get(s);
				for (int j=0; j<roundedItemsToTake.get(s); j++) {
					Path path = paths.get(start+j);
					currentFold.put(path, s);
				}
				startIndex.put(s, start+roundedItemsToTake.get(s));
				remaining.put(s, remaining.get(s)-roundedItemsToTake.get(s));
			}
			folds.add(currentFold);
		}

		return folds;
	}
	
	private double testNB(Map<Path, Sentiment> training, Map<Path, Sentiment> testing) throws IOException {
		Map<Sentiment, Double> classProbabilities = implementation2.calculateClassProbabilities(training);

		Map<String, Map<Sentiment, Double>> smoothedLogProbs = implementation2
				.calculateSmoothedLogProbs(training);
		

		
		Map<Path, Sentiment> smoothedNBPredictions = implementation2.naiveBayes(testing.keySet(),
				smoothedLogProbs, classProbabilities);
		

		return implementation1.calculateAccuracy(testing, smoothedNBPredictions);
	}
	
	@Override
	public double[] crossValidate(List<Map<Path, Sentiment>> folds) throws IOException {
		double[] results = new double[folds.size()];
		for (int i=0; i<folds.size(); i++) {
			Map<Path, Sentiment> training = new HashMap<Path, Sentiment>();
			for (int j=0; j<folds.size(); j++) {
				if (j != i) {
					training.putAll(folds.get(j));
				}
			}
			Map<Path, Sentiment> testing = folds.get(i);
			results[i] = testNB(training, testing);
		}
		return results;
	}

	@Override
	public double cvAccuracy(double[] scores) {
		return Arrays.stream(scores).average().orElse(0);
	}

	@Override
	public double cvVariance(double[] scores) {
		double mu = cvAccuracy(scores);
		return Arrays.stream(scores).map(e -> (e-mu)*(e-mu)).average().orElse(0);
	}

}
