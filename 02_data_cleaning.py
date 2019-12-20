import pandas as pd
df = pd.read_csv(r"D:\UNSW\tweets.csv")

# delete duplicate tweets
df = df.drop_duplicates(['id'])

# get data types
df.dtypes

# change data type to datetime
df = df.astype({"created_at":"datetime64[ns]"})
# df['co_lon'] = df['co_lon'].astype(float)

# get total number of every source
df.source.value_counts()

# get total number of tweets with goe-tags
df.coordinates.value_counts()

# get tweets from Aus
df = df[df['place_country'] == 'Australia']

# get English tweets
df = df[df['lang'] == 'en']

# use re.sub to implement this
# example like this
# change all the non-alphabet to single space

import re
name = "alex@bingnan#is a good boy!!!! Hahahaha-?-=-=-=+_+_+_+_+$%$%#@#@#$!#@)(!$&)*#(@)*$#(@467749237492365)"
name_alpha = re.sub("[^a-zA-Z]", " ", name)
print(name_alpha)
# Eliminate duplicate whitespaces
print(re.sub(r"\s+", " ", name_alpha))

# convert all the characters into lower case
for ind in df.index:
    df.loc[ind]['user_location'] = df.loc[ind]['user_location'].lower()
    df.loc[ind]['text'] = df.loc[ind]['text'].lower()

# delete links
def remove_urls (vTEXT):
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
    return(vTEXT)

for i in range(20):
    print(df.iloc[i]['text'])
    print(remove_urls(df.iloc[i]['text']))

# get related tweets
import re
keywords = ['flu', 'influenza', 'fever', 'cough', 'sore throat', 'runny nose', 'stuffy nose', 'cold', 'headache']
def word_extraction(sentence):
	words = re.sub("[^\w]", " ",  sentence).split()
	cleaned_text = [w.lower() for w in words]
	return cleaned_text

count = 0
is_flu = ['No']*dft.shape[0]
for i in range(len(dft)):
    for kw in keywords:
        if kw in word_extraction(dft.iloc[i]['text'].lower()):
            count += 1
            is_flu[i] = "Yes"
            break
print(count)
