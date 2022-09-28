#!/usr/bin/python3.9

import numpy as np
import warnings

with open("alice.txt") as f:
    data = f.read()

alphabet = list(set(data))
alphabet_idx_lookup = {}
for i, char in enumerate(alphabet):
    alphabet_idx_lookup[char] = i


# Generate bigram probability matrix
bigram_matrix = np.zeros((len(alphabet), len(alphabet)), dtype=float)
first_letter_matrix = np.zeros(len(alphabet), dtype=float)
all_letter_matrix = np.zeros(len(alphabet), dtype=float)

last_char = None
for char in data:
    char = alphabet_idx_lookup[char]
    
    if last_char is not None:
        bigram_matrix[last_char, char] += 1
    
    all_letter_matrix[char] += 1
    if last_char is None or alphabet[last_char] == " ":
        first_letter_matrix[char] += 1
    
    last_char = char

# Normalize distributions
bigram_matrix /= np.sum(bigram_matrix, axis=1)[:, np.newaxis]
first_letter_matrix /= np.sum(first_letter_matrix)
all_letter_matrix /= np.sum(all_letter_matrix)

# Helpful pre-computations
with warnings.catch_warnings():
    # Catch divide-by-zero warnings
    # If the value really is zero, we'll never pick it anyway
    warnings.simplefilter("ignore")
    H_cond = -np.log2(bigram_matrix) * bigram_matrix
    H_first = -np.log2(first_letter_matrix) * first_letter_matrix
    H = -np.log2(all_letter_matrix) * all_letter_matrix

def generate_word():
    # Pick the first letter of the word according to first_letter_matrix
    current = np.random.choice(np.arange(len(alphabet)), p=first_letter_matrix)
    word = ""

    entropy = H_first[current]

    while (alphabet[current] != " "):
        word += alphabet[current]
        # Pick the next letter according to bigram_matrix
        nxt = np.random.choice(np.arange(len(alphabet)), p=bigram_matrix[current, :])

        # Add to entropy in accordance with the chain rule
        # NOTE: Assuming P(X_n|X_n-1, X_n-2, ..., X_1) = P(X_n|X_n-1)
        #       (Markov assumption)
        entropy += H_cond[current, nxt]

        current = nxt

    
    return word, entropy

words, entropies = zip(*list(generate_word() for _ in range(10000)))

# Sort words by entropy
words = list(np.array(words, dtype="object")[np.argsort(entropies)[::-1]])

print(words[:10])

# ['lokendinfisemakitheerminthaing', 'soprerokishaimucerulitinlishormad', 'ssatheastomaishersemeridouryo', 'thtoundshengrathechithey', 'appouteyithithemigucryphale', 'ishooushewilinioupotoumits', 'waingoulickithicoutim', 'waderplousoulingereeme', 'heskllofiriteryoventhntllld', 'sentheesearithailyore']