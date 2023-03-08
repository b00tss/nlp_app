import re, contractions, nltk, spacy
import numpy as np
import pandas as pd
from nltk.corpus import stopwords

dialogs = pd.read_csv("data/data.csv", names=["msg"], header=None, ) #nrows=90)
#dialogs = dialogs.iloc[0:500]

# remove url
dialogs['msg'] = dialogs['msg'].apply(lambda x: re.split('https:\/\/.*', str(x))[0])

# remove hashtags and mentions
dialogs['msg'] = dialogs['msg'].apply(lambda x: ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",x).split()))

# Remove punctuation
dialogs['msg'] = dialogs['msg'].map(lambda x: re.sub('[,\.!?]', ' ', x))

# removing numbers from strings of specified 
dialogs['msg'] = dialogs['msg'].str.replace('\d+', '')

# remove emoticons
filter_char = lambda c: ord(c) < 256
dialogs['msg'] = dialogs['msg'].apply(lambda x: ''.join(filter(filter_char, x)))

# remove contractions
dialogs['msg'] = dialogs['msg'].apply(lambda x: contractions.fix(x))

# Unique words
#uniqueWords = list(set(' '.join(dialogs['msg']).lower().split(' ')))
#count = len(uniqueWords)

# Total words
#dialogs['total_words'] = dialogs['msg'].str.split().str.len()
#totalWordCount = dialogs['total_words'].sum()

# Remove stopwords
stopwords = nltk.corpus.stopwords.words('english')
dialogs['msg'] = dialogs['msg'].apply(lambda x: ' '.join([w for w in x.split() if w.lower() not in stopwords]))

# lemmatization
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
allowed_postags=['NOUN',]
dialogs['msg'] = dialogs['msg'].apply(lambda x: ' '.join([token.lemma_ if token.lemma_ not in ['-PRON-'] else '' for token in nlp(x) if token.pos_ in allowed_postags]))

# drop empty strings
dialogs['msg'].replace('', np.nan, inplace=True)
dialogs.dropna(subset=['msg'], inplace=True)

#store and read the data file
dialogs.to_pickle('./data/all_docs.pkl')
