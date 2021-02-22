package uk.ac.cam.cl.jbs52.exercises;

import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.stream.Collectors;

import uk.ac.cam.cl.mlrd.exercises.markov_models.AminoAcid;
import uk.ac.cam.cl.mlrd.exercises.markov_models.Feature;
import uk.ac.cam.cl.mlrd.exercises.markov_models.HMMDataStore;
import uk.ac.cam.cl.mlrd.exercises.markov_models.HiddenMarkovModel;
import uk.ac.cam.cl.mlrd.exercises.markov_models.IExercise9;

public class Exercise9 implements IExercise9 {

	public static class CrossValidator {
		private static <A> void shuffle(Random rng, List<A> list) {
			for (int i = 0; i < list.size(); i++) {
				int index = rng.nextInt(list.size());
				A tmp = list.get(index);
				list.set(index, list.get(i));
				list.set(i, tmp);
			}
		}

		public static <A> List<List<A>> splitCVRandom(List<A> dataSet, int foldCount, int seed) {
			List<A> entries = new ArrayList<A>(dataSet);
			shuffle(new Random(seed), entries);
			int maxFoldSize = (int) Math.ceil(entries.size() / foldCount);

			int currentFoldSize = 0;
			List<A> currentFold = null;
			List<List<A>> folds = new ArrayList<List<A>>();

			for (int i = 0; i < entries.size(); i++) {
				if (currentFold == null || currentFoldSize >= maxFoldSize) {
					currentFold = new ArrayList<A>();
					folds.add(currentFold);
					currentFoldSize = 0;
				}
				A entry = entries.get(i);
				currentFold.add(entry);
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
	public HiddenMarkovModel<AminoAcid, Feature> estimateHMM(List<HMMDataStore<AminoAcid, Feature>> sequencePairs)
			throws IOException {
		Map<Feature, Map<Feature, Double>> transitionMatrix = new HashMap<Feature, Map<Feature, Double>>();
		Map<Feature, Map<AminoAcid, Double>> emissionMatrix = new HashMap<Feature, Map<AminoAcid, Double>>();

		Map<Feature, Double> counts = new HashMap<Feature, Double>();

		for (HMMDataStore<AminoAcid, Feature> sequence : sequencePairs) {
			for (int i = 0; i < sequence.observedSequence.size(); i++) {
				Feature type = sequence.hiddenSequence.get(i);
				AminoAcid roll = sequence.observedSequence.get(i);

				Double count = counts.get(type);
				if (count == null) {
					count = 1.0;
				} else {
					count++;
				}
				counts.put(type, count);

				Map<AminoAcid, Double> e = emissionMatrix.get(type);
				if (e == null) {
					e = new HashMap<AminoAcid, Double>();
					emissionMatrix.put(type, e);
				}
				Double c = e.get(roll);
				if (c == null) {
					c = 1.0;
				} else {
					c++;
				}
				e.put(roll, c);

				if (i < sequence.observedSequence.size() - 1) {
					Map<Feature, Double> t = transitionMatrix.get(type);
					if (t == null) {
						t = new HashMap<Feature, Double>();
						transitionMatrix.put(type, t);
					}
					Feature next = sequence.hiddenSequence.get(i + 1);
					Double a = t.get(next);
					if (a == null) {
						a = 1.0;
					} else {
						a++;
					}
					t.put(next, a);
				}
			}
		}

		for (Feature type1 : Feature.values()) {
			Map<Feature, Double> trans = transitionMatrix.get(type1);
			if (trans == null) {
				trans = new HashMap<Feature, Double>();
				transitionMatrix.put(type1, trans);
			}
			Map<AminoAcid, Double> emm = emissionMatrix.get(type1);
			if (emm == null) {
				emm = new HashMap<AminoAcid, Double>();
				emissionMatrix.put(type1, emm);
			}
			Double count = counts.get(type1);
			if (count == null) {
				count = 0.0;
			}
			for (Feature type2 : Feature.values()) {
				Double a = trans.get(type2);
				if (a == null) {
					a = 0.0;
				}
				a /= count;
				trans.put(type2, a);
			}

			for (AminoAcid roll : AminoAcid.values()) {
				Double b = emm.get(roll);
				if (b == null) {
					b = 0.0;
				}
				b /= count;
				emm.put(roll, b);
			}
		}

		return new HiddenMarkovModel<AminoAcid, Feature>(transitionMatrix, emissionMatrix);
	}

	@Override
	public List<Feature> viterbi(HiddenMarkovModel<AminoAcid, Feature> model, List<AminoAcid> observedSequence) {
		List<Map<Feature, Feature>> psi = new ArrayList<Map<Feature, Feature>>();
		List<Map<Feature, Double>> delta = new ArrayList<Map<Feature, Double>>();

		Map<Feature, Map<Feature, Double>> a = model.getTransitionMatrix();
		Map<Feature, Map<AminoAcid, Double>> b = model.getEmissionMatrix();

		for (int t = 0; t < observedSequence.size(); t++) {
			Map<Feature, Feature> previousStates = new HashMap<Feature, Feature>();
			Map<Feature, Double> pathProbs = new HashMap<Feature, Double>();

			psi.add(previousStates);
			delta.add(pathProbs);

			AminoAcid obs = observedSequence.get(t);
			List<Feature> possiblePrevious = new ArrayList<Feature>(Arrays.asList(Feature.values()));
			Feature[] possibleCurrent = Feature.values();

			possiblePrevious.add(null);

			for (Feature current : possibleCurrent) {
				double max = Double.NEGATIVE_INFINITY;
				Feature mostLikely = null;
				for (Feature previous : possiblePrevious) {
					double trans = Math.log((current == Feature.START && previous == null ? 1.0
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

		List<Feature> prediction = new ArrayList<Feature>();
		Feature next = Feature.END;
		prediction.add(next);

		for (int t = psi.size() - 1; t >= 1; t--) {
			next = psi.get(t).get(next);
			prediction.add(0, next);
		}

		return prediction;
	}

	@Override
	public Map<List<Feature>, List<Feature>> predictAll(HiddenMarkovModel<AminoAcid, Feature> model,
			List<HMMDataStore<AminoAcid, Feature>> testSequencePairs) throws IOException {
		return testSequencePairs.stream()
				.collect(Collectors.toMap(x -> x.hiddenSequence, x -> this.viterbi(model, x.observedSequence)));
	}

	@Override
	public double precision(Map<List<Feature>, List<Feature>> true2PredictedMap) {
		double predictedW = 0.0;
		double correctlyPredictedW = 0.0;

		for (Map.Entry<List<Feature>, List<Feature>> entry : true2PredictedMap.entrySet()) {
			List<Feature> ground = entry.getKey();
			List<Feature> prediction = entry.getValue();
			for (int i = 0; i < prediction.size(); i++) {
				if (prediction.get(i) == Feature.MEMBRANE) {
					predictedW++;
					if (ground.get(i) == Feature.MEMBRANE) {
						correctlyPredictedW++;
					}
				}
			}
		}

		return correctlyPredictedW / predictedW;
	}

	@Override
	public double recall(Map<List<Feature>, List<Feature>> true2PredictedMap) {
		double trueW = 0.0;
		double correctlyPredictedW = 0.0;

		for (Map.Entry<List<Feature>, List<Feature>> entry : true2PredictedMap.entrySet()) {
			List<Feature> ground = entry.getKey();
			List<Feature> prediction = entry.getValue();
			for (int i = 0; i < ground.size(); i++) {
				if (ground.get(i) == Feature.MEMBRANE) {
					trueW++;
					if (prediction.get(i) == Feature.MEMBRANE) {
						correctlyPredictedW++;
					}
				}
			}
		}

		return correctlyPredictedW / trueW;
	}

	@Override
	public double fOneMeasure(Map<List<Feature>, List<Feature>> true2PredictedMap) {
		double p = precision(true2PredictedMap);
		double r = recall(true2PredictedMap);
		return 2 * p * r / (p + r);
	}

}
