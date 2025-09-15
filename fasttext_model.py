import fasttext

# Save sentences to a text file (one sentence per line)
with open("training_data.txt", "w", encoding="utf-8") as f:
    f.write("I love machine learning\n")
    f.write("FastText is an improvement over Word2Vec\n")

# Train FastText model (skipgram)
model = fasttext.train_unsupervised("training_data.txt", model='skipgram', dim=100, ws=3, minCount=1)

# Get word vector
vector = model.get_word_vector("learning")
print("Vector for 'learning':", vector)

# Save and load model
model.save_model("fasttext_model.bin")
model = fasttext.load_model("fasttext_model.bin")
