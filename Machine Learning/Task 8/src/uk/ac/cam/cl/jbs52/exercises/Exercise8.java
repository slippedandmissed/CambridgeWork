package uk.ac.cam.cl.jbs52.exercises;

import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.stream.Collectors;

import uk.ac.cam.cl.mlrd.exercises.markov_models.DiceRoll;
import uk.ac.cam.cl.mlrd.exercises.markov_models.DiceType;
import uk.ac.cam.cl.mlrd.exercises.markov_models.HMMDataStore;
import uk.ac.cam.cl.mlrd.exercises.markov_models.HiddenMarkovModel;
import uk.ac.cam.cl.mlrd.exercises.markov_models.IExercise8;

public class Exercise8 implements IExercise8 {
	
	public static class CrossValidator {
		private static <A> void shuffle(Random rng, List<A> list) {
			for (int i = 0; i < list.size(); i++) {
				int index = rng.nextInt(list.size());	
				A tmp = list.get(index);
				list.set(index, list.get(i));
				list.set(i, tmp);
			}
		}
		
		public static <A> List<Map<Path, A>> splitCVRandom(Map<Path, A> dataSet, int foldCount, int seed) {
			List<Map.Entry<Path, A>> entries = new ArrayList<Map.Entry<Path, A>>(dataSet.entrySet());
			shuffle(new Random(seed), entries);
			int maxFoldSize = (int) Math.ceil(entries.size() / foldCount);

			int currentFoldSize = 0;
			Map<Path, A> currentFold = null;
			List<Map<Path, A>> folds = new ArrayList<Map<Path, A>>();

			for (int i = 0; i < entries.size(); i++) {
				if (currentFold == null || currentFoldSize >= maxFoldSize) {
					currentFold = new HashMap<Path, A>();
					folds.add(currentFold);
					currentFoldSize = 0;
				}
				Map.Entry<Path, A> entry = entries.get(i);
				currentFold.put(entry.getKey(), entry.getValue());
				currentFoldSize++;
			}

			return folds;
		}
	}

	private <A, B, C> C getTwiceOrElse(Map<A, Map<B, C>> map, A key1, B key2, C fallback) {
		Map<B, C> inner = map.get(key1);
		if (inner == null) {
			return fallback;
		}
		C c = inner.get(key2);
		if (c == null) {
			return fallback;
		}
		return c;
	}

	private <A, B> B getTwiceOrElse(List<Map<A, B>> list, int key1, A key2, B fallback) {
		if (key1 < 0 || key1 >= list.size()) {
			return fallback;
		}
		Map<A, B> inner = list.get(key1);
		B b = inner.get(key2);
		if (b == null) {
			return fallback;
		}
		return b;
	}

	@Override
	public List<DiceType> viterbi(HiddenMarkovModel<DiceRoll, DiceType> model, List<DiceRoll> observedSequence) {

		List<Map<DiceType, DiceType>> psi = new ArrayList<Map<DiceType, DiceType>>();
		List<Map<DiceType, Double>> delta = new ArrayList<Map<DiceType, Double>>();

		Map<DiceType, Map<DiceType, Double>> a = model.getTransitionMatrix();
		Map<DiceType, Map<DiceRoll, Double>> b = model.getEmissionMatrix();

		for (int t = 0; t < observedSequence.size(); t++) {
			Map<DiceType, DiceType> previousStates = new HashMap<DiceType, DiceType>();
			Map<DiceType, Double> pathProbs = new HashMap<DiceType, Double>();

			psi.add(previousStates);
			delta.add(pathProbs);

			DiceRoll obs = observedSequence.get(t);
			List<DiceType> possiblePrevious = new ArrayList<DiceType>(Arrays.asList(DiceType.values()));
			DiceType[] possibleCurrent = DiceType.values();

			possiblePrevious.add(null);

			for (DiceType current : possibleCurrent) {
				double max = Double.NEGATIVE_INFINITY;
				DiceType mostLikely = null;
				for (DiceType previous : possiblePrevious) {
					double trans = Math.log((current == DiceType.START && previous == null ? 1.0
							: getTwiceOrElse(a, previous, current, 0.0)));
					double emm = Math.log(getTwiceOrElse(b, current, obs, 0.0));
					double prevDel = getTwiceOrElse(delta, t - 1, previous, 1.0);
					double p = trans + emm + prevDel;
					if (p > max) {
						max = p;
						mostLikely = previous;
					}
				}
				previousStates.put(current, mostLikely);
				pathProbs.put(current, max);
			}
		}

		List<DiceType> prediction = new ArrayList<DiceType>();
		DiceType next = DiceType.END;
		prediction.add(next);

		for (int t = psi.size() - 1; t >= 1; t--) {
			next = psi.get(t).get(next);
			prediction.add(0, next);
		}

		return prediction;
	}

	@Override
	public Map<List<DiceType>, List<DiceType>> predictAll(HiddenMarkovModel<DiceRoll, DiceType> model,
			List<Path> testFiles) throws IOException {
		return HMMDataStore.loadDiceFiles(testFiles).stream()
				.collect(Collectors.toMap(x -> x.hiddenSequence, x -> this.viterbi(model, x.observedSequence)));
	}

	@Override
	public double precision(Map<List<DiceType>, List<DiceType>> true2PredictedMap) {

		double predictedW = 0.0;
		double correctlyPredictedW = 0.0;

		for (Map.Entry<List<DiceType>, List<DiceType>> entry : true2PredictedMap.entrySet()) {
			List<DiceType> ground = entry.getKey();
			List<DiceType> prediction = entry.getValue();
			for (int i = 0; i < prediction.size(); i++) {
				if (prediction.get(i) == DiceType.WEIGHTED) {
					predictedW++;
					if (ground.get(i) == DiceType.WEIGHTED) {
						correctlyPredictedW++;
					}
				}
			}
		}

		return correctlyPredictedW / predictedW;
	}

	@Override
	public double recall(Map<List<DiceType>, List<DiceType>> true2PredictedMap) {
		double trueW = 0.0;
		double correctlyPredictedW = 0.0;

		for (Map.Entry<List<DiceType>, List<DiceType>> entry : true2PredictedMap.entrySet()) {
			List<DiceType> ground = entry.getKey();
			List<DiceType> prediction = entry.getValue();
			for (int i = 0; i < ground.size(); i++) {
				if (ground.get(i) == DiceType.WEIGHTED) {
					trueW++;
					if (prediction.get(i) == DiceType.WEIGHTED) {
						correctlyPredictedW++;
					}
				}
			}
		}

		return correctlyPredictedW / trueW;
	}

	@Override
	public double fOneMeasure(Map<List<DiceType>, List<DiceType>> true2PredictedMap) {
		double p = precision(true2PredictedMap);
		double r = recall(true2PredictedMap);
		return 2 * p * r / (p + r);
	}

}
