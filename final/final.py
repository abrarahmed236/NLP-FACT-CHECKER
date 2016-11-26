'Importing libraries'
import os, math
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import Counter
from collections import OrderedDict

'Initializations'
print('\n\nWorking: Inititialization')
corpus_root = '../Data'
#corpus_root = '../stateoftheunionaddresses'
stopwords = stopwords.words('english')
stopwords.sort()
corpus = {}
tf_dict = {}
idf_dict = {}
tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
stemmer = PorterStemmer()

'Reading Data'
print('Working: Reading Data files into a dictionary')
for filename in os.listdir(corpus_root):
    file = open(os.path.join(corpus_root, filename), 'r')
    filetext = file.read()
    corpus[filename] = str(filetext)
    corpus = OrderedDict(sorted(corpus.items(), key = lambda corpus: corpus[0]))

'Tokenizing, Stemming and TF'
print('Working: Tokenizing, Stemming and TF')
for filename in corpus:
    filetext = corpus[filename]
    terms = tokenizer.tokenize(filetext)
    terms = [term.lower() for term in terms]
    terms = [term for term in terms if term not in stopwords] 
    terms = [stemmer.stem(term) for term in terms]

    tf_dict[filename] = {}    
    tf_dict[filename] = Counter(terms)

'Finding IDF'
print('Working: Finding IDF of each word')
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
    Fact = input ("\n\nEnter Fact to be verified:-------------------\n")
    if Fact == 0:
        break
    trueness = 0
    counter = 0
    for file in corpus:
        similarity =cossim(Fact,file)
        #print("Similarity: ",similarity)
        trueness += similarity
        counter += 1
    trueness /= counter
    print("")
    print("Trueness: ", trueness)
    threshold = 0.04 # not true train this
    if trueness >= threshold:
        print("THE FACT IS TRUE")
    else:
    	print("THE FACT IS FALSE")
    print("---------------------------------------------")

    
