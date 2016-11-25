'Taking user input'
testVar = input ("Ask user for something.\n")
print(testVar)


'reading from data files to dictionary'
import os
corpus={}
corpus_root = 'data'
for filename in os.listdir(corpus_root):
    print (filename)
    file = open(os.path.join(corpus_root, filename), 'r')
    filetext = file.read()
    corpus[filename] = str(filetext)
    print (filetext)