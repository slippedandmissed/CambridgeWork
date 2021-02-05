package uk.ac.cam.cl.jbs52.exercises;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import uk.ac.cam.cl.mlrd.exercises.sentiment_detection.IExercise1;
import uk.ac.cam.cl.mlrd.exercises.sentiment_detection.Sentiment;
import uk.ac.cam.cl.mlrd.exercises.sentiment_detection.Tokenizer;

public class Exercise1 implements IExercise1{
	
	public static class SentimentWithIntensity {
		public static enum Intensity {
			WEAK,
			STRONG;
		}
		
		public final Sentiment sentiment;
		public final Intensity intensity;
		
		public SentimentWithIntensity (Sentiment sentiment, Intensity intensity) {
			this.sentiment = sentiment;
			this.intensity = intensity;
		}
	}
		
	public static Map<String, SentimentWithIntensity> loadSentimentLexiconWithIntensity (Path lexiconFile) throws IOException{
		Map<String, SentimentWithIntensity> map = new HashMap<String, SentimentWithIntensity>();
		BufferedReader reader = Files.newBufferedReader(lexiconFile);
		String currentLine = null;
		while ((currentLine = reader.readLine()) != null) {
			String[] parts = currentLine.split(" ");
			String word = parts[0].split("=")[1];
			Sentiment polarity = parts[2].split("=")[1].equals("positive") ? Sentiment.POSITIVE : Sentiment.NEGATIVE;
			SentimentWithIntensity.Intensity intensity = parts[1].split("=")[1].equals("weak") ? SentimentWithIntensity.Intensity.WEAK : SentimentWithIntensity.Intensity.STRONG;
			map.put(word, new SentimentWithIntensity(polarity, intensity));
		}
		return map;

	}

	
	public static Map<String, Sentiment> loadSentimentLexicon (Path lexiconFile) throws IOException{
		Map<String, Sentiment> map = new HashMap<String, Sentiment>();
		Map<String, SentimentWithIntensity> sentimentsWithIntensities = loadSentimentLexiconWithIntensity(lexiconFile);
		for (String string: sentimentsWithIntensities.keySet()) {
			map.put(string, sentimentsWithIntensities.get(string).sentiment);
		}
		return map;
	}

	@Override
	public Map<Path, Sentiment> simpleClassifier(Set<Path> testSet, Path lexiconFile) throws IOException {
		Map<String, Sentiment> lexicon = loadSentimentLexicon(lexiconFile);
		Map<Path, Sentiment> classifications = new HashMap<Path, Sentiment>();
		for (Path path: testSet) {
			int judgement = 0;
			List<String> words = Tokenizer.tokenize(path);
			for (String word: words) {
				Sentiment polarity = lexicon.get(word);
				if (polarity != null) {
					judgement += polarity == Sentiment.POSITIVE ? 1 : -1;
				}
			}
			classifications.put(path, judgement >= 0 ? Sentiment.POSITIVE : Sentiment.NEGATIVE);
		}
		return classifications;
	}
	
	@Override
	public Map<Path, Sentiment> improvedClassifier(Set<Path> testSet, Path lexiconFile) throws IOException {
		final double STRONG_MULTIPLIER = 10;
		final double COUNT_MULTIPLIER = 0.03;
		
		Map<String, SentimentWithIntensity> lexicon = loadSentimentLexiconWithIntensity(lexiconFile);
		Map<Path, Sentiment> classifications = new HashMap<Path, Sentiment>();
		for (Path path: testSet) {
			int judgement = 0;
			Map<String, Integer> count = new HashMap<String, Integer>();
			List<String> words = Tokenizer.tokenize(path);
			for (String word: words) {
				SentimentWithIntensity sentimentWithIntensity = lexicon.get(word);
				if (sentimentWithIntensity != null) {
					Integer c = count.get(word);
					if (c == null) {
						c = 0;
					}
					count.put(word, ++c);
					judgement += (sentimentWithIntensity.sentiment == Sentiment.POSITIVE ? 1 : -1) * ((sentimentWithIntensity.intensity == SentimentWithIntensity.Intensity.STRONG? STRONG_MULTIPLIER : 1) + (c*COUNT_MULTIPLIER));
				}
			}
			classifications.put(path, judgement >= 0 ? Sentiment.POSITIVE : Sentiment.NEGATIVE);
		}
		return classifications;
	}

	@Override
	public double calculateAccuracy(Map<Path, Sentiment> trueSentiments, Map<Path, Sentiment> predictedSentiments) {
		double correct = 0;
		for (Path path: trueSentiments.keySet()) {
			if (trueSentiments.get(path) == predictedSentiments.get(path)) {
				correct++;
			}
		}
		return correct / trueSentiments.size();
	}

    
    
}
