import sys
import csv
import logging
import os
import gensim
import smart_open

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# tokanized line joined by spaces to job number mapping.
TOKANIZED_SENTANCE_TO_JOB_ID_MAPPING = {}

def read_corpus(f, tokens_only=False):
	for i, line in enumerate(f):
		should_map = False
		has_map_tilda = line.split('~')
		if len(has_map_tilda) == 2:
			# Special case.
			line = has_map_tilda[0]
			should_map = True
		tokens = gensim.utils.simple_preprocess(line)
		if should_map:
			TOKANIZED_SENTANCE_TO_JOB_ID_MAPPING[str(i)] = {'sentance': [' '.join(tokens)], 'job_code': has_map_tilda[1].strip() } 
		if tokens_only:
			yield tokens
		else:
			# For training data, add tags
			yield gensim.models.doc2vec.TaggedDocument(tokens, [i])

# Custom corpus from open data.
with open('corpus_dump', 'r') as fh:
	corpus = fh.readlines()

train_corpus = list(read_corpus(corpus))

with open('preserved_mappings', 'w') as fh:
	fh.write(str(TOKANIZED_SENTANCE_TO_JOB_ID_MAPPING))

# Snippet of the corpus.
print(train_corpus[:3])

model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=40)
model.build_vocab(train_corpus)
model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)

test_sentance = 'extroverts are fun, friendly & down to earth. They like talking and helping people'
raw_tokens = gensim.utils.simple_preprocess(test_sentance)
print(raw_tokens)
query_vector = model.infer_vector(raw_tokens)
sims = model.dv.most_similar([query_vector], topn=len(model.dv))

print('Test Document (%s):' % ' '.join(raw_tokens));

print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
for label, index in [('MOST', 0), ('MEDIAN', len(sims)//2), ('LEAST', len(sims) - 1)]:
	print(u'%s %s: «%s»\n' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))

print("number of similar things: %s" % len(sims))
# Want top 10 similar things.
for i in range(0, 20):
	document_id = sims[i][0]
	if str(document_id) in TOKANIZED_SENTANCE_TO_JOB_ID_MAPPING:
		print("most similar match found at: %s with docId: %s" % (str(i), str(document_id)))
		print(TOKANIZED_SENTANCE_TO_JOB_ID_MAPPING[str(document_id)])
		break
	else:
		print("no match for sim index: " + str(i))

MODEL_NAME = "doc2vec_model_final"
model.save(MODEL_NAME)
print("Saved model! " + MODEL_NAME)
