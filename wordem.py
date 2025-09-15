from gensim.models import Word2Vec
from gensim.utils import simple_preprocess


# Sample dataset (list of sentences)
sentences = [
    "Natural language processing is fascinating.",
    "Word embeddings capture semantic meaning.",
    "Machine learning and deep learning are part of AI.",
    "Text data requires preprocessing before training models.",
    "Word2Vec is a popular method for word embeddings."
]

# Tokenize sentences
tokenized_sentences = [simple_preprocess(sentence) for sentence in sentences]

# Train Word2Vec model
model = Word2Vec(sentences=tokenized_sentences, vector_size=100, window=5, min_count=1, workers=4)

# Save the model
model.save("word2vec.model")

# Load the model
loaded_model = Word2Vec.load("word2vec.model")

# Find similar words
similar_words = loaded_model.wv.most_similar("word", topn=5)
print("Words similar to 'word':", similar_words)

# Get vector representation of a word
word_vector = loaded_model.wv["word"]
print("Vector representation of 'word':", word_vector[:10])  # Print first 10 values for readability