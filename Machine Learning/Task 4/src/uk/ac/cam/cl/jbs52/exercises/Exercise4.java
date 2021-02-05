package uk.ac.cam.cl.jbs52.exercises;

import java.io.BufferedReader;
import java.io.IOException;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import uk.ac.cam.cl.mlrd.exercises.sentiment_detection.IExercise4;
import uk.ac.cam.cl.mlrd.exercises.sentiment_detection.Sentiment;
import uk.ac.cam.cl.mlrd.exercises.sentiment_detection.Tokenizer;

public class Exercise4 implements IExercise4 {

	public static class SentimentWithIntensity {
		public static enum Intensity {
			WEAK, STRONG;
		}

		public final Sentiment sentiment;
		public final Intensity intensity;

		public SentimentWithIntensity(Sentiment sentiment, Intensity intensity) {
			this.sentiment = sentiment;
			this.intensity = intensity;
		}
	}

	public static Map<String, SentimentWithIntensity> loadSentimentLexiconWithIntensity(Path lexiconFile)
			throws IOException {
		Map<String, SentimentWithIntensity> map = new HashMap<String, SentimentWithIntensity>();
		BufferedReader reader = Files.newBufferedReader(lexiconFile);
		String currentLine = null;
		while ((currentLine = reader.readLine()) != null) {
			String[] parts = currentLine.split(" ");
			String word = parts[0].split("=")[1];
			Sentiment polarity = parts[2].split("=")[1].equals("positive") ? Sentiment.POSITIVE : Sentiment.NEGATIVE;
			SentimentWithIntensity.Intensity intensity = parts[1].split("=")[1].equals("weak")
					? SentimentWithIntensity.Intensity.WEAK
					: SentimentWithIntensity.Intensity.STRONG;
			map.put(word, new SentimentWithIntensity(polarity, intensity));
		}
		return map;

	}

	@Override
	public Map<Path, Sentiment> magnitudeClassifier(Set<Path> testSet, Path lexiconFile) throws IOException {
		final double STRONG_MULTIPLIER = 2;

		Map<String, SentimentWithIntensity> lexicon = loadSentimentLexiconWithIntensity(lexiconFile);
		Map<Path, Sentiment> classifications = new HashMap<Path, Sentiment>();
		for (Path path : testSet) {
			int judgement = 0;
			Map<String, Integer> count = new HashMap<String, Integer>();
			List<String> words = Tokenizer.tokenize(path);
			for (String word : words) {
				SentimentWithIntensity sentimentWithIntensity = lexicon.get(word);
				if (sentimentWithIntensity != null) {
					Integer c = count.get(word);
					if (c == null) {
						c = 0;
					}
					count.put(word, ++c);
					judgement += (sentimentWithIntensity.sentiment == Sentiment.POSITIVE ? 1 : -1)
							* (sentimentWithIntensity.intensity == SentimentWithIntensity.Intensity.STRONG
									? STRONG_MULTIPLIER
									: 1);
				}
			}
			classifications.put(path, judgement >= 0 ? Sentiment.POSITIVE : Sentiment.NEGATIVE);
		}
		return classifications;
	}

	private BigDecimal choose(int n, int r) {
		int a = Math.min(r, n - r);
		int b = Math.max(r, n - r);
		BigDecimal total = BigDecimal.ONE;
		for (int i = b + 1; i <= n; i++) {
			total = total.multiply(BigDecimal.valueOf(i));
		}
		for (int i = 1; i <= a; i++) {
			total = total.divide(BigDecimal.valueOf(i));
		}
		return total;
	}

	@Override
	public double signTest(Map<Path, Sentiment> actualSentiments, Map<Path, Sentiment> classificationA,
			Map<Path, Sentiment> classificationB) {
		int plus = 0, minus = 0, nvll = 0;
		for (Path path : actualSentiments.keySet()) {
			Sentiment ground = actualSentiments.get(path);
			Sentiment a = classificationA.get(path);
			Sentiment b = classificationB.get(path);
			if (a == b) {
				nvll++;
			} else if (a == ground) {
				plus++;
			} else {
				minus++;
			}
		}
		int hNull = (int) Math.ceil(nvll / 2.0);
		int n = 2 * hNull + plus + minus;
		int k = hNull + Math.min(plus, minus);
		double q = 0.5;
		double sum = 0;
		for (int i = 0; i <= k; i++) {
			sum += choose(n, i).multiply(BigDecimal.valueOf(Math.pow(q, i)* Math.pow(1 - q, n - i))).doubleValue();
		}

		return 2 * sum;
	}

}
