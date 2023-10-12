import sys
import gzip

from collections import Counter
from stemmer import *
from stopword import *
from tokenizer import *

def process(inputZipFile, OutFile, tokenize, stoplist, stemming):
    original = []
    # First read from file into array, creates array of strings
    # spaces
    in_file = gzip.open(inputZipFile, 'rt')
    for line in in_file:
        original.extend(line.strip().split())
    out = original.copy()

    if tokenize == 'fancy':
        out = tokenizer(original)
    else:
        for i, item in enumerate(original):
            out[i] = [item]
    
    if stoplist == 'yesStop':
        out = removeStopWords(out)
    
    if stemming == 'porterStem':
        out = stemmer(out)
        
    # create output files
    
    # create tokens output
    out_tokens = open(OutFile+'-tokens.txt', 'w')
    for i, elem in enumerate(original):
        out_tokens.write(elem)
        for x in out[i]:
            out_tokens.write(" " + str(x))
        out_tokens.write("\n")
    
    #create heaps
    out_heap = open(OutFile+'-heaps.txt', 'w')
    tokenCounter = Counter()
    heap = flatten(out)
    count = 0
    for word in heap:
        if word == '':
            continue
        tokenCounter.update([str(word)])
        count += 1
        if(count % 10 == 0):
            out_heap.write(str(sum(tokenCounter.values())) + " " + str(len(tokenCounter.keys())) + "\n")
    
    #create stats
    out_stats = open(OutFile+'-stats.txt', 'w')
    out_stats.write(str(sum(tokenCounter.values())) + "\n")
    out_stats.write(str(len(tokenCounter.keys())) + "\n")
    toPrint = sorted(tokenCounter.items(), key= lambda item: (-item[1], item[0]))
    for tup in toPrint:
        out_stats.write(tup[0] + " " + str(tup[1]) + "\n")
    # print(len(Counter(original).items()))
    # print(out)    
    

if __name__ == '__main__':
    # Read arguments from command line; or use sane defaults for IDE.
    argv_len = len(sys.argv)
    inputFile = sys.argv[1] if argv_len >= 2 else "P1-train.gz"
    # inputFile = sys.argv[1] if argv_len >= 2 else "sense-and-sensibility.gz"
    outputFilePrefix = sys.argv[2] if argv_len >= 3 else "outPrefix"
    outputFilePrefix = sys.argv[2] if argv_len >= 3 else "senseOut"
    tokenize_type = sys.argv[3] if argv_len >= 4 else "fancy"
    stoplist_type = sys.argv[4] if argv_len >= 5 else "yesStop"
    stemming_type = sys.argv[5] if argv_len >= 6 else "porterStem"

    # Below is stopword list
    stopword_lst = stopword_lst = ["a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
                    "has", "he", "in", "is", "it", "its", "of", "on", "that", "the", "to",
                    "was", "were", "with"]
    
    process(inputFile, outputFilePrefix, tokenize_type, stoplist_type, stemming_type)