import numpy as np
import math, nltk, re
from collections import defaultdict
from collections import Counter
from math import sqrt

PROBLEM_WORDS = [ line.strip() for line in open('problem.slim.txt') ] #找skip by gram

lm = nltk.WordNetLemmatizer()

corpus = [line.replace('\n', '') for line in open('ef_edit.txt',encoding='UTF-8').readlines()]

# generate all the skip-bigram of "edit tag"
def list_to_skipgram(words, maxdist=5, problem_words=PROBLEM_WORDS):
    splits = words.split()
    result = []
    editTags = re.findall(r'\[\S*|\{\S*',words)

    for problem_word in problem_words:
        if problem_word in splits:
            probIndex = splits.index(problem_word)    
            result.extend([(problem_word,tag,splits.index(tag)-probIndex)  for tag in editTags if abs(probIndex - splits.index(tag))<=maxdist])
    return result

# implement skip bigram
skgm = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
         
for words in corpus:  
    for item in list_to_skipgram(words):
        skgm[item[0]][item[1]][str(item[2])]+=1 

skipbigram_static = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda:0)))
# you can calculate all the required number first (freq, std, spread, etc.) 
for head,tags in skgm.items():
    for tag,pos in tags.items():
        skipbigram_static[head][tag]['freq'] = sum(list(pos.values()))
        skipbigram_static[head][tag]['N'] = len(list(pos.keys()))
        skipbigram_static[head][tag]['avg_f'] = skipbigram_static[head][tag]['freq'] / skipbigram_static[head][tag]['N']
        skipbigram_static[head][tag]['avg_p'] = skipbigram_static[head][tag]['freq'] / 10
        skipbigram_static[head][tag]['std'] = math.sqrt((skipbigram_static[head][tag]['freq'] - skipbigram_static[head][tag]['avg_f'])**2 / 10)
        
        p_freq_sumofsq = sum([(p_freq - skipbigram_static[head][tag]['avg_p'])**2 for p_freq in list(pos.values())])
        skipbigram_static[head][tag]['spread'] = math.sqrt(p_freq_sumofsq / 10)


### test node
#skipbigram_static['arrive']['{+at+}'] 
# {'freq': 73, 'avg_f': 18.25, 'avg_p': 7.3, 'spread': 15.20983234621605}


for key in ['explain' , 'discuss' , 'reach']: # problem words #完成三個condition
#for key in ['arrive']:
    result = []

    for tag,value in skipbigram_static[key].items():
        if value['std']!= 0 and (value['freq'] - value['avg_f']) / value['std'] >= 1 and value['spread'] >= 1 :
            pos = Counter(skgm[key][tag])
            for dsit,freq in pos.items():
                if freq > value['avg_p'] + math.sqrt(value['spread']): result.append((key,tag,dsit,freq))
                    

    print(result)

'''
Result: 

explain [-you-] (1, 4) 距離1 文本中有4個
explain [-for>>to+} (-1, 4)
explain {+will+} (-1, 4)
explain {+to+} (1, 31)
------
discuss [-about-] (1, 11)
discuss {+the+} (1, 5)
------
reach {+the+} (1, 3)
reach {+to+} (-1, 4)
------
'''
