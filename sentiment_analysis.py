from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd

tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

#build a scraper to collect reviews
r = requests.get('https://www.yelp.com/biz/social-brew-cafe-pyrmont')
soup = BeautifulSoup(r.text, 'html.parser')
regex = re.compile('.*comment.*') #isolate page elements with the class "comment"
results = soup.find_all('p', {'class':regex}) #pull out all the classes inside a p tag
reviews = [result.text for result in results] #scrape the reviews
#print(reviews)

#load reviews into a data frame
df = pd.DataFrame(np.array(reviews), columns=['review'])

#df['review'].iloc[0]

#return asentiment score when given a review
def sentiment_score(review):
    tokens = tokenizer.encode(review, return_tensors='pt')
    #print(tokens)
    result = model(tokens)
    #print(int(torch.argmax(result.logits))+1) #transform numerical sentiment into a 1 = 5 integer value. 1 is worst, 5 is best.
    return int(torch.argmax(result.logits))+1

#loop through reviews and attach a sentiment column to the data frame
df['sentiment'] = df['review'].apply(lambda x: sentiment_score(x[:512])) #there is a limit of 512 tokens allowed in the computation of the sentiment score
#df['review'].iloc[3]

print(df.head()) #get some printed feedback of the data frame header, which is the first 5 elements

total_sentiments = 0