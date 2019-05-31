from collections import defaultdict, Counter
import sys
import re
import fileinput
import copy
max_distance = 5


# Input:
# 	sent: list of string tokens ex. ['Happy', 'to', 'deal', 'with', 'lab', 'work', '!']
#	n : length of ngrams ex. 3 get all trigrams
# Output:
#	a list of all n-grams given input sent and length n
#	ex. ngrams(['Happy', 'to', 'deal', 'with', 'lab', 'work', '!'], 2)
#		return ['Happy to', 'to deal', 'deal with', 'with lab' ...]
def ngrams(sent, n):
    return [ ' '.join(x) for x in zip(*[sent[i:] for i in range(n) if i <= len(sent) ] ) ]


# read file from pipeline
# get all n-grams with length from 2 ~ 5 
# print result
# ex. happy to     1
#.    to deal.     1
'''   
for line in fileinput.input():
    for n in range(2,6):
        ngrams_counts = Counter(ngrams(line.strip().split(' '),n))
        for ngram in (ngrams_counts.items()):
            n , nc = ngram[0] , ngram[1]
            print(n +'\t'+str(nc))

'''

for line in fileinput.input():
	infos = line.strip().split('\t')
	words = infos[0].split()
	tags = infos[2].split()
	chunks = infos[3].split()


	result = list()
	chunk = list()

	for i,item in enumerate(chunks):
		tag = item[0]
		
		if tag != 'O':
			if tag == 'H':
				if len(chunk)!=0:
					chunk.append(i)
					result.append(copy.deepcopy(chunk))
					chunk=[]
				else:
					chunk.append(i)
			else:
				chunk.append(i)


	w = ''
	t = ''
	c = ''

	for c_index in result:
		if len(c_index) != 1: 
			for index in c_index:
				w = w + ' ' + words[index]
				t = t + ' ' + tags[index]
				c = c + ' ' + chunks[index]

		print(w + '\t' + t + '\t' + c + '\t' + '1')
		w = ''
		t = ''
		c = ''

