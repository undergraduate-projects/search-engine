from gensim.models import KeyedVectors

print("loading word2vec model...")
# load pre-trained word vectors
tc_wv_model = KeyedVectors.load_word2vec_format('data/embedding.txt', binary=False)
print("word2vec model loaded.")

# load stop words
with open('data/stop_words', 'r', encoding='utf-8') as f:
    stop_words = set(f.read().split('\n'))