'imports'
import os,math
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import Counter

'initializers'
stopwords = stopwords.words('english')
stopwords.sort()
corpus = {}
tf_dict = {}
idf_dict = {}
tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
stemmer = PorterStemmer()
qstring = 'Rajesh is a good boy. He loves playing football. Football is his life.'

'tokenize, stop removal stem'
qterms = tokenizer.tokenize(qstring)
qterms = [qterm.lower() for qterm in qterms]
qterms = [qterm for qterm in qterms if qterm not in stopwords]
qterms = [stemmer.stem(qterm) for qterm in qterms]

'TF'
tf_qterms = {}
tf_qterms = Counter(qterms)


tf_wt = {}    
for term in tf_qterms:
    print(term)
    tf_wt[term] = 1 + math.log10(tf_qterms[term])
    print(tf_wt)