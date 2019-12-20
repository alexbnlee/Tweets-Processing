# Stanford NER
article = '''
Asian shares skidded on Tuesday after a rout in tech stocks put Wall Street to the sword, while a 
sharp drop in oil prices and political risks in Europe pushed the dollar to 16-month highs as investors dumped 
riskier assets. MSCI’s broadest index of Asia-Pacific shares outside Japan dropped 1.7 percent to a 1-1/2 
week trough, with Australian shares sinking 1.6 percent. Japan’s Nikkei dived 3.1 percent led by losses in 
electric machinery makers and suppliers of Apple’s iphone parts. Sterling fell to $1.286 after three straight 
sessions of losses took it to the lowest since Nov.1 as there were still considerable unresolved issues with the
European Union over Brexit, British Prime Minister Theresa May said on Monday.'''

import nltk
from nltk.tag import StanfordNERTagger

# print('NTLK Version: %s' % nltk.__version__)

stanford_ner_tagger = StanfordNERTagger(
    r"D:\Twitter Data\Data\NER\stanford-ner-2018-10-16\classifiers\english.muc.7class.distsim.crf.ser.gz",
	r"D:\Twitter Data\Data\NER\stanford-ner-2018-10-16\stanford-ner-3.9.2.jar"
)

results = stanford_ner_tagger.tag(article.split())

# print('Original Sentence: %s' % (article))
for result in results:
    tag_value = result[0]
    tag_type = result[1]
    if tag_type != 'O':
        print('Value: %s\nType: %s' % (tag_value, tag_type))
        
# spaCy
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
doc = nlp(article)
for X in doc.ents:
	print('Value: %s, Type: %s' % (X.text, X.label_))
  
# NLTK
def fn_preprocess(art):
    art = nltk.word_tokenize(art)
    art = nltk.pos_tag(art)
    return art
art_processed = fn_preprocess(article)
print(art_processed)

# get continuous words starting with a capital letter    
import re
pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|·|！|…|（'
a = "I am Alex Lee. I am from Denman Prospect and I love this place very much. We don't like apple. The big one is good."
# our goal is getting 'I', 'Alex Lee', 'Denman Prospect', 'I'

def get_capital(sentence):
    sections = [s.strip() for s in re.split(pattern, sentence)]
    
    caps = []
    
    for sec in sections:
        tmp = []
        for w in sec.split():
            if w[0].isupper():
                tmp.append(w)
            elif len(tmp) > 0:
                caps.append(tmp)
                tmp = []
        if len(tmp) > 0:
            caps.append(tmp)
            tmp = []
    
    caps = [' '.join(c) for c in caps]
    
    return list(set(caps))
        
print(get_capital(a))

# Similar with the above method, but also delete stopwords
# method 1
import re
import nltk
from nltk.corpus import stopwords
pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|·|！|…|（'
a = "I am Alex Lee. I am from Denman Prospect and I love this place very much. We don't like apple. The big one is good."
# our goal is getting 'I', 'Alex Lee', 'Denman Prospect', 'I'

def get_capital(sentence):
    sections = [s.strip() for s in re.split(pattern, sentence)]
    
    caps = []
    
    for sec in sections:
        tmp = []
        for w in sec.split():
            if w[0].isupper():
                tmp.append(w)
            elif len(tmp) > 0:
                caps.append(tmp)
                tmp = []
        if len(tmp) > 0:
            caps.append(tmp)
            tmp = []
    
    caps = list(set([' '.join(c) for c in caps]))
    
    caps = [c for c in caps if c.lower() not in stopwords.words('english')]
    
    return list(set(caps))
        
print(get_capital(a))

# method 2 (better, based on NLTK)
import nltk
from nltk.corpus import stopwords
a = "I am Alex Lee. I am from Denman Prospect and I love this place very much. We don't like apple. The big one is good."
tokens = nltk.word_tokenize(a)
caps = []
for i in range(1, 4):
    for eles in nltk.ngrams(tokens, i):
        length = len(list(eles))
        for j in range(length):
            if eles[j][0].islower() or not eles[j][0].isalpha():
                break
            elif j == length - 1:
                caps.append(' '.join(list(eles)))

caps = list(set(caps))
caps = [c for c in caps if c.lower() not in stopwords.words('english')]
print(caps)
