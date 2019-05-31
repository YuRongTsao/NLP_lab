import math, re
from collections import Counter, defaultdict

# tokenize text and get words list
def words(text): return re.findall(r'\w+|\.|,|\?|\!|\:|\;', text.lower())

# get all bigrams
def bigrams(text):
    word_list = words(text)
    return [word_list[i] +' '+ word_list[i+1] for i in range(len(word_list)-1)]

uni_count = Counter(words(open('big.txt').read()))
bi_count = Counter(bigrams(open('big.txt').read()))


# P(A|B), given B, calculate A probability
# return bigram probability
def bigram_prob():
    prob_model = defaultdict(lambda: 0)
    prob_model.update({key : value / uni_count[words(key)[0]] for key,value in bi_count.items()})
    return prob_model
    
bigram_LM = bigram_prob()

# add-one smooth
V = len(list(uni_count.keys()))
def add1_smooth(bigram):
    return math.log(1 / uni_count[words(bigram)[0]] + V)
    
# calculate the sentence probability
# when prob. of bigram == 0, remember to use smooth
def sentence_prob(sentence):
    s_bigrams = bigrams(sentence)
    prob_list = [bigram_LM[text] if bigram_LM[text]!=0 else add1_smooth(text) for text in s_bigrams] 
    return sum(map(math.log10,prob_list))

if __name__ == "__main__":
    lm = sentence_prob("He is looking a new job.")
    print(lm)
