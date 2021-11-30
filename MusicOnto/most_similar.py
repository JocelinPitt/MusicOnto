import spacy
import numpy as np
nlp = spacy.load('en_core_web_lg')

'''def most_similar(word, topn=5):
    word = nlp.vocab[str(word)]
    print(word)
    queries = [
        w for w in word.vocab
        if w.is_lower == word.is_lower and np.count_nonzero(w.vector)
    ]
    print(queries)

    by_similarity = sorted(queries, key=lambda w: word.similarity(w), reverse=True)
    return [(w.lower_, w.similarity(word)) for w in by_similarity[:topn+1] if w.lower_ != word.lower_]'''

from sense2vec import Sense2Vec
# Loading pretrained model
s2v = Sense2Vec().from_disk("s2v_reddit_2015_md/s2v_old")

query = "apple|NOUN"
vector = s2v[query]
s2v.most_similar(query)

'''import spacy
from sense2vec import Sense2VecComponent

nlp = spacy.load("en_core_web_sm")
s2v = Sense2VecComponent(nlp.vocab).from_disk("s2v_reddit_2015_md\s2v_old")
nlp.add_pipe(s2v)

doc = nlp("A sentence about natural language processing.")
assert doc[3:6].text == "natural language processing"
freq = doc[3:6]._.s2v_freq
vector = doc[3:6]._.s2v_vec
mostsimilar = doc[3:6]._.s2v_most_similar(3)

print(mostsimilar)

#ms = nlp.vocab.vectors.most_similar(np.asarray([nlp.vocab.vectors[nlp.vocab.strings['king']]]), n=10)
#print([nlp.vocab.strings[w] for w in ms[0][0]])'''


'''# Imports
from scipy.spatial import distance
import spaCy

# Load the spacy vocabulary
nlp = spacy.load("en_core_web_lg")

# Format the input vector for use in the distance function
# In this case we will artificially create a word vector from a real word ("frog")
# but any derived word vector could be used
input_word = "frog"
p = np.array([nlp.vocab[input_word].vector])

# Format the vocabulary for use in the distance function
ids = [x for x in nlp.vocab.vectors.keys()]
vectors = [nlp.vocab.vectors[x] for x in ids]
vectors = np.array(vectors)

# *** Find the closest word below ***
closest_index = distance.cdist(p, vectors).argmin()
word_id = ids[closest_index]
output_word = nlp.vocab[word_id].text
# output_word is identical, or very close, to the input word'''