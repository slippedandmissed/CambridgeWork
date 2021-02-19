package uk.ac.cam.cl.mlrd.testing;

import java.io.IOException;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

//TODO: Replace with your package.
import uk.ac.cam.cl.jbs52.exercises.Exercise7;
import uk.ac.cam.cl.jbs52.exercises.Exercise8;
import uk.ac.cam.cl.mlrd.exercises.markov_models.DiceRoll;
import uk.ac.cam.cl.mlrd.exercises.markov_models.DiceType;
import uk.ac.cam.cl.mlrd.exercises.markov_models.HMMDataStore;
import uk.ac.cam.cl.mlrd.exercises.markov_models.HiddenMarkovModel;
import uk.ac.cam.cl.mlrd.exercises.markov_models.IExercise7;
import uk.ac.cam.cl.mlrd.exercises.markov_models.IExercise8;

public class Exercise8Tester {

	static final Path dataDirectory = Paths.get("data/dice_dataset");

	public static void main(String[] args)
			throws IOException, ClassNotFoundException, InstantiationException, IllegalAccessException {

		List<Path> sequenceFiles = new ArrayList<>();
		try (DirectoryStream<Path> files = Files.newDirectoryStream(dataDirectory)) {
			for (Path item : files) {
				sequenceFiles.add(item);
			}
		} catch (IOException e) {
			throw new IOException("Cant access the dataset.", e);
		}

		// Use for testing the code
//		Collections.shuffle(sequenceFiles, new Random(0));
//		int testSize = sequenceFiles.size() / 10;
//		List<Path> devSet = sequenceFiles.subList(0, testSize);
//		List<Path> testSet = sequenceFiles.subList(testSize, 2 * testSize);
//		List<Path> trainingSet = sequenceFiles.subList(testSize * 2, sequenceFiles.size());
		// But:
		// TODO: Replace with cross-validation for the tick.

		Map<Path, HMMDataStore<DiceRoll, DiceType>> corpus = sequenceFiles.stream()
				.collect(Collectors.toMap(Function.identity(), arg0 -> {
					try {
						return HMMDataStore.loadDiceFile(arg0);
					} catch (IOException e) {
						e.printStackTrace();
						return null;
					}
				}));

		IExercise7 implementation7 = (IExercise7) new Exercise7();
		IExercise8 implementation = (IExercise8) new Exercise8();

		List<Map<Path, HMMDataStore<DiceRoll, DiceType>>> folds = Exercise8.CrossValidator.splitCVRandom(corpus, 10, 0);

		double precision = 0.0;
		double recall = 0.0;
		double fOne = 0.0;

		for (int i = 0; i < folds.size(); i++) {
			List<Path> trainingPaths = new ArrayList<Path>();
			List<Path> testPaths = new ArrayList<Path>();
			for (int j = 0; j < folds.size(); j++) {
				if (i == j) {
					testPaths.addAll(folds.get(j).keySet());
				} else {
					trainingPaths.addAll(folds.get(j).keySet());
				}
			}
			HiddenMarkovModel<DiceRoll, DiceType> model = implementation7.estimateHMM(trainingPaths);
			Map<List<DiceType>, List<DiceType>> predictions = implementation.predictAll(model, testPaths);
			precision += implementation.precision(predictions);
			recall += implementation.recall(predictions);
			fOne += implementation.fOneMeasure(predictions);
		}

		precision /= folds.size();
		recall /= folds.size();
		fOne /= folds.size();

		System.out.println("Average precision:");
		System.out.println(precision);
		System.out.println();

		System.out.println("Average recall");
		System.out.println(recall);
		System.out.println();

		System.out.println("Average fOneMeasure");
		System.out.println(fOne);
		System.out.println();

//		HMMDataStore<DiceRoll, DiceType> data = HMMDataStore.loadDiceFile(devSet.get(0));
//		List<DiceType> predicted = implementation.viterbi(model, data.observedSequence);
//		System.out.println("True hidden sequence:");
//		System.out.println(data.hiddenSequence);
//		System.out.println();
//
//		System.out.println("Predicted hidden sequence:");
//		System.out.println(predicted);
//		System.out.println();
//
//		Map<List<DiceType>, List<DiceType>> true2PredictedMap = implementation.predictAll(model, devSet);
//		double precision = implementation.precision(true2PredictedMap);
//		System.out.println("Prediction precision:");
//		System.out.println(precision);
//		System.out.println();
//
//		double recall = implementation.recall(true2PredictedMap);
//		System.out.println("Prediction recall:");
//		System.out.println(recall);
//		System.out.println();
//
//		double fOneMeasure = implementation.fOneMeasure(true2PredictedMap);
//		System.out.println("Prediction fOneMeasure:");
//		System.out.println(fOneMeasure);
//		System.out.println();
	}
}
