import os, math, time
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import Counter

corpus={}
corpus_root = 'data'
stopwords = stopwords.words('english')
stopwords.sort()
tf_dict = {}
idf_dict = {}
tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
stemmer = PorterStemmer()

for filename in os.listdir(corpus_root):
    file = open(os.path.join(corpus_root, filename), 'r'
    filetext = file.read()
    corpus[filename] = str(filetext)

for filename in corpus:
    filetext = corpus[filename]
    terms = tokenizer.tokenize(filetext)
    terms = [term.lower() for term in terms]
    terms = [term for term in terms if term not in stopwords
    terms = [stemmer.stem(term) for term in terms
    
    tf_dict[filename] = {}
    tf_dict[filename] = Counter(terms)
    print (tf_dict)

temp = tf_dict

a = ' '
for filename in tf_dict:
    for word in tf_dict[filename]:
        count = 0
        try:
            for file in temp:
                    if word in temp[file]:
                    count = count + 1
        except KeyError:
            a=a+' '
        idf_dict[word] = math.log10(len(tf_dict) / float(count)
print (idf_dict)