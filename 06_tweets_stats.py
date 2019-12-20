# weekly tweets

import pandas as pd
from datetime import datetime
 
#fn = r"D:\OneDrive - UNSW\tweets_flu.csv"
#df = pd.read_csv(fn)

ws = []
for i in range(len(df)):
    t = df.iloc[i]['created_at']
    w = datetime.strptime(t, "%Y-%m-%d %H:%M:%S").strftime("%W")
    ws.append(w)

df['ws'] = ws

wsu = df['ws'].value_counts()
 
wss = []
 
for i in wsu.index:
    wss.append((i, wsu[i]))

wss = sorted(wss, key=lambda x:x[0])

print(wss)

# sort tuple based on the first element
wss = sorted(wss, key=lambda x:x[0])
print(wss)

# save data in to txt file
fn = r"D:\Data\CSV\weekly_tweets.csv"
fo = open(fn, "w+")
for e in wss:
    fo.write(e[0] + ", " + str(e[1]) + "\n")
fo.close()

# tweets realted to flu
import re
keywords = ['flu', 'influenza', 'fever', 'cough', 'sore throat', 'runny nose', 'stuffy nose', 'cold', 'headache']
def word_extraction(sentence):
	words = re.sub("[^\w]", " ",  sentence).split()
	cleaned_text = [w.lower() for w in words]
	return cleaned_text

count = 0
for i in range(len(df)):
    for kw in keywords:
        if kw in word_extraction(str(df.iloc[i]['text']).lower()):
            count += 1
            break
print(count)

# user number
import json
import os
import codecs

folderpath = r"D:\Twitter Data\Data"
files = os.listdir(folderpath)
os.chdir(folderpath)

fo = open(r"D:\Twitter Data\Data\test\user_id.csv", "w")
fo.write("\ufeff")
fo.write("user_id")
count = 0

for file in files:
    # determine is file or directory
    if os.path.isdir(file):
        continue
        
    count += 1
    print(count, ":", file)

    tweets_file = open(file, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            csv_text = "\n"
            csv_text += tweet["user"]["id_str"]
            fo.write(csv_text)
        except:
            continue
    
fo.close()   

import pandas as pd
dff = pd.read_csv(r"D:\Twitter Data\Data\test\user_id.csv")
dff.head()

dfff = dff.drop_duplicates()
dfff.shape

# processing with progress bar
import sys,time

total = 153
 
for i in range(total):

    if i+1 == total:
        percent = 100.0
        print('Progress: %s [%d/%d]'%(str(percent)+'%',i+1,total),end='\n')
    else:
        percent = round(1.0 * i / total * 100,2)
        print('Progress: %s [%d/%d]'%(str(percent)+'%',i+1,total),end='\r')
    time.sleep(0.01)
    
