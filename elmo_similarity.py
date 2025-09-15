import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

# Download NLTK tokenizer if not available
nltk.download('punkt')

# Load a modern sentence embedding model (alternative to ELMo)
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_word_embeddings(sentence):
    """
    Generates word embeddings for a given sentence using SentenceTransformers.

    Args:
        sentence (str): A sentence.

    Returns:
        dict: A dictionary mapping words to their embeddings.
    """
    words = word_tokenize(sentence)
    word_embeddings = model.encode(words)  # Generate embeddings for each token
    return dict(zip(words, word_embeddings))

def calculate_cosine_similarity(vec1, vec2):
    """
    Calculates the cosine similarity between two vectors.

    Args:
        vec1 (np.array): First vector.
        vec2 (np.array): Second vector.

    Returns:
        float: Cosine similarity score.
    """
    return 1 - cosine(vec1, vec2) if np.linalg.norm(vec1) and np.linalg.norm(vec2) else 0.0

# Sample sentences
sentences = [
    "The cat sat on the mat.",
    "My feline friend rested on the rug."
]

# Get embeddings for individual words
sentence1_embeddings = get_word_embeddings(sentences[0])
sentence2_embeddings = get_word_embeddings(sentences[1])

# Define word pairs to compare
word_pairs = [("cat", "feline"), ("mat", "rug")]

# Compute cosine similarities
for word1, word2 in word_pairs:
    if word1 in sentence1_embeddings and word2 in sentence2_embeddings:
        similarity = calculate_cosine_similarity(sentence1_embeddings[word1], sentence2_embeddings[word2])
        print(f"Cosine similarity between '{word1}' and '{word2}': {similarity:.4f}")
    else:
        print(f"One of the words ('{word1}' or '{word2}') was not found in tokenized sentences.")
