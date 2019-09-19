import os
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import multiprocessing


corpus_file = "./news-sentences-cut.txt"

output1 = './wiki_seg.50.model'
output2 = './wiki_seg.50.vector'


print('-----------Train Word2Vec-------------\n')
print('multiprocessing.cpu_count: {}\n'.format(multiprocessing.cpu_count()))

model = Word2Vec(LineSentence(corpus_file), size=50,workers=multiprocessing.cpu_count())

model.save(output1)
model.wv.save_word2vec_format(output2, binary=False)

		