#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
from collections import defaultdict

NGRAM_API_URI = "https://{0}.linggle.com/query/"
EXP_API_URI = "https://{0}.linggle.com/example/"


class Linggle:
    def __init__(self, ver='www'):
        self.ver = ver

    def __getitem__(self, query):
        return self.search(query)

    def search(self, query): #回傳query的所有結果
        query = query.replace('/', '@')
        req = requests.get(NGRAM_API_URI.format(self.ver) + query)
        results = req.json()
        return results.get('ngrams', [])

    def get_example(self, ngram_str):
        res = requests.post(EXP_API_URI.format(self.ver), json={'ngram': ngram_str})
        if res.status_code == 200:
            result = res.json()
            return result.get("examples", [])
        return []

def readFile(path):
    with open(path,encoding='utf-8') as f:
        return json.load(f)

def getAllCombination(head):
    return ling.search(head + ' _')

def getTag(words,w2):
    totalCount = 0 
    tags = {}
    result = ''

    if w2 in prep:
        return ' ' + w2
    else:
        if words in bigram and words.upper() in biposgram:
            totalCount = bigram[words]
            tags = biposgram[words.upper()]
        elif w2 in unigram and words.upper() in uniposgram :
            totalCount = unigram[w2]
            tags = uniposgram[words.upper()]
        else:
            return result

        probs = {key : value/totalCount for key,value in tags.items()}
        result = max(probs, key=lambda k: probs[k])
        if result in change and result !='DT':
            result = change[result]
            tagWords[result].append(w2)
    return result

def getWord3(words,w2):
    comb = [item[0] for item in getAllCombination(w2)]
    result = defaultdict(lambda:0)
    for word in comb:
        words = word.split()
        w_2 = words[1] 
        result[getTag(word,w_2)] += 1

    return result

def getExamples(patterns):
    result = [] 
    for pattern in patterns:
        split = pattern.split()
        w1 = split[0]

        p2 = split[1]
        p3 = split[2]
        
        w2 = tagWords[' '+ p2][0] if p2 in tagWords else p2
        w3 = tagWords[' '+ p3][0] if p3 in tagWords else p3

        result.append(ling.get_example(w1+' '+w2+' '+w3)[0])
    return result


def init():
    bigram = readFile(r'D:\Tammy\University\graduate\107-spring\NLP\lab_4\bi.json')
    unigram = readFile(r'D:\Tammy\University\graduate\107-spring\NLP\lab_4\un.json')
    biposgram = readFile(r'D:\Tammy\University\graduate\107-spring\NLP\lab_4\pos.ngram.json')
    uniposgram = readFile(r'D:\Tammy\University\graduate\107-spring\NLP\lab_4\uni.pos.json')
    change = readFile(r'D:\Tammy\University\graduate\107-spring\NLP\lab_4\change.json')
    return bigram,unigram,biposgram,uniposgram,change

bigram,unigram,biposgram,uniposgram,change = init()
ling = Linggle()
example = ling.get_example('happy n.') 
head = 'happy'
comb = getAllCombination(head)
result = defaultdict(lambda:defaultdict(lambda:defaultdict()))
pattern = defaultdict(lambda:0)
tagWords = defaultdict(list)

boringWords = {'the','a'}
prep = {'to','with','about','for','at',}

for item in comb:
    words = item[0]
    splits = words.split()
    w1 = splits[0]
    w2 = splits[1]

    if w2 not in boringWords:
        tag = getTag(words,w2)
        w3 = getWord3(words,w2)
        result[w1][tag] = w3

pattern = {(head + tag1 + tag2) : count for head,tag1s in result.items() for tag1,tag2s in tag1s.items() for tag2,count in tag2s.items() if tag1!='' and tag2!=''} 
        
values = list(pattern.values())
keys = list(pattern.keys())
topPatterns = [keys[values.index(value)] for value in sorted(values,reverse = True)[:3]]

print(getExamples(topPatterns))

print('hi')


    

    



