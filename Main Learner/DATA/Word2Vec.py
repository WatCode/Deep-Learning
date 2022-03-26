from gensim.models import Word2Vec
from nltk.tokenize import sent_tokenize, word_tokenize

filer = open("SHAKESPEARERAW.txt", "r").read().replace("\n", " ")

data = []

for i in sent_tokenize(filer):
    temp = []
    
    for j in word_tokenize(i):
        temp.append(j.lower())
        
    data.append(temp)
    
model = Word2Vec(data, min_count=1, window=5)

print(model.wv.key_to_index.keys())