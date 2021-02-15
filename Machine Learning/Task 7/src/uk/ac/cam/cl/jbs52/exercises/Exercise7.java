package uk.ac.cam.cl.jbs52.exercises;

import java.io.IOException;
import java.nio.file.Path;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

import uk.ac.cam.cl.mlrd.exercises.markov_models.DiceRoll;
import uk.ac.cam.cl.mlrd.exercises.markov_models.DiceType;
import uk.ac.cam.cl.mlrd.exercises.markov_models.HMMDataStore;
import uk.ac.cam.cl.mlrd.exercises.markov_models.HiddenMarkovModel;
import uk.ac.cam.cl.mlrd.exercises.markov_models.IExercise7;

public class Exercise7 implements IExercise7 {

	@Override
	public HiddenMarkovModel<DiceRoll, DiceType> estimateHMM(Collection<Path> sequenceFiles) throws IOException {
		Collection<HMMDataStore<DiceRoll, DiceType>> sequences = HMMDataStore.loadDiceFiles(sequenceFiles);

		Map<DiceType, Map<DiceType, Double>> transitionMatrix = new HashMap<DiceType, Map<DiceType, Double>>();
		Map<DiceType, Map<DiceRoll, Double>> emissionMatrix = new HashMap<DiceType, Map<DiceRoll, Double>>();

		Map<DiceType, Double> counts = new HashMap<DiceType, Double>();

		for (HMMDataStore<DiceRoll, DiceType> sequence : sequences) {
			for (int i = 0; i < sequence.observedSequence.size(); i++) {
				DiceType type = sequence.hiddenSequence.get(i);
				DiceRoll roll = sequence.observedSequence.get(i);

				Double count = counts.get(type);
				if (count == null) {
					count = 1.0;
				} else {
					count++;
				}
				counts.put(type, count);

				Map<DiceRoll, Double> e = emissionMatrix.get(type);
				if (e == null) {
					e = new HashMap<DiceRoll, Double>();
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
					Map<DiceType, Double> t = transitionMatrix.get(type);
					if (t == null) {
						t = new HashMap<DiceType, Double>();
						transitionMatrix.put(type, t);
					}
					DiceType next = sequence.hiddenSequence.get(i + 1);
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

		for (DiceType type1 : DiceType.values()) {
			Map<DiceType, Double> trans = transitionMatrix.get(type1);
			if (trans == null) {
				trans = new HashMap<DiceType, Double>();
				transitionMatrix.put(type1, trans);
			}
			Map<DiceRoll, Double> emm = emissionMatrix.get(type1);
			if (emm == null) {
				emm = new HashMap<DiceRoll, Double>();
				emissionMatrix.put(type1, emm);
			}
			Double count = counts.get(type1);
			if (count == null) {
				count = 0.0;
			}
			for (DiceType type2 : DiceType.values()) {
				Double a = trans.get(type2);
				if (a == null) {
					a = 0.0;
				}
				a /= count;
				trans.put(type2, a);
			}

			for (DiceRoll roll : DiceRoll.values()) {
				Double b = emm.get(roll);
				if (b == null) {
					b = 0.0;
				}
				b /= count;
				emm.put(roll, b);
			}
		}

		return new HiddenMarkovModel<DiceRoll, DiceType>(transitionMatrix, emissionMatrix);
	}

}
