from collections import defaultdict, Counter
import sys
import fileinput
import re
import operator

# read data from pipeline 
# accumulates all n-grams 
# print result in the following format
# ex. happy to    245
ngram_counts = defaultdict(Counter)


shows = []
ngram_counts = defaultdict(lambda:0)
tagNames = dict()

for line in fileinput.input():
	infos = line.split('\t')
	words = infos[0]
	tags = infos[1]
	chunks = infos[2]

	ngram_counts[words] += 1
	tagNames[words] = tags + '\t' + chunks

for words in ngram_counts:
	print(words +'\t'+ tagNames[words] + '\t' + str(ngram_counts[words]))
	
	
