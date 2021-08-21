# import gensim.models as gensimModels
from gensim.models.doc2vec import Doc2Vec

def doc2vec_loader():
	# Doc2Vec model trained on wikipedia articles using distributed bag of words.
	# TODO: maybe try skipgram? 
	model = Doc2Vec.load("enwiki_dbow/doc2vec.bin")
	return model

m = doc2vec_loader()
print(m)