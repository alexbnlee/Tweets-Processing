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

        
