'Importing libraries'
import os, math
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import Counter
from collections import OrderedDict

'Initializations'
corpus_root = 'Data'
#corpus_root = 'stateoftheunionaddresses'
stopwords = stopwords.words('english')
stopwords.sort()
corpus = {}
tf_dict = {}
idf_dict = {}
tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
stemmer = PorterStemmer()

'Reading Data'
print('Reading Data files into a dictionary \n')
for filename in os.listdir(corpus_root):
    file = open(os.path.join(corpus_root, filename), 'r')
    filetext = file.read()
    corpus[filename] = str(filetext)
    corpus = OrderedDict(sorted(corpus.items(), key = lambda corpus: corpus[0]))

'Tokenizing, Stemming and TF'
print('Tokenizing, Stemming and TF\n')
for filename in corpus:
    filetext = corpus[filename]
    terms = tokenizer.tokenize(filetext)
    terms = [term.lower() for term in terms]
    terms = [term for term in terms if term not in stopwords] 
    terms = [stemmer.stem(term) for term in terms]

    tf_dict[filename] = {}    
    tf_dict[filename] = Counter(terms)

'Finding IDF'
print('Finding IDF of each word \n')
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
            a = a + ' '
        
        idf_dict[word] = math.log10(len(tf_dict) / float(count))

'Getting string vector'
def getqvec(qstring):  
    qterms = tokenizer.tokenize(qstring)
    qterms = [qterm.lower() for qterm in qterms]
    qterms = [qterm for qterm in qterms if qterm not in stopwords]
    qterms = [stemmer.stem(qterm) for qterm in qterms]
    
    tf_qterms = {}
    tf_qterms = Counter(qterms)
    
    tf_wt = {}    
    for term in tf_qterms:
        tf_wt[term] = 1 + math.log10(tf_qterms[term])
        
    tf_idf_wt= {}
    for term in tf_wt:
        if term in idf_dict:
            tf_idf_wt[term] = tf_wt[term] * idf_dict[term]
        else:
            tf_idf_wt[term] = 0
        
    d = 0
    for term in tf_idf_wt:
        d = d + math.pow(tf_idf_wt[term], 2)
    
    normd = math.sqrt(d)
    qvec = {}
    for term in tf_idf_wt:
        try:
            qvec[term] = tf_idf_wt[term]/normd        
        except ZeroDivisionError:
            qvec[term] = 0
    return qvec

'getting file vector'
def gettfidfvec(filename):
    tf_wt = {}
    tf_idf_file = {}
    for term in tf_dict[filename]:
        tf_term = tf_dict[filename][term]
        tf_wt[term] = 1 + math.log10(tf_term)
        tf_idf_file[term] = tf_wt[term] * idf_dict[term]
        
    d = 0
    for term in tf_idf_file:
        d = d + pow(tf_idf_file[term], 2)
    
    normd = math.sqrt(d)    
    tfidfvec = {}
    for term in tf_idf_file:
        try:
            tfidfvec[term] = tf_idf_file[term]/normd
        except ZeroDivisionError:
            tfidfvec[term] = 0
    return tfidfvec

'Cosine Similarity'
def cossim(query, filename):
    cosine = 0
    tfidf_q = getqvec(query)
    tfidf_f = gettfidfvec(filename)

    common = set(tfidf_q) & set(tfidf_f)
    a = 0
    
    for word in common:
        try:
            cosine = cosine + (tfidf_q[word] * tfidf_f[word])
            
        except KeyError:
            a = a + 1
    
    return cosine

'Main Function'
while 1:
    Fact = input ("Enter Fact to be verified.\n")
    if Fact == 0:
        break
    sum = 0
    counter = 0
    for file in corpus:
         cossim(Fact,file)
    
