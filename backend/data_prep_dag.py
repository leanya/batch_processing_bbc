from bs4 import BeautifulSoup
import pandas as pd
import requests
from sqlalchemy import create_engine
import sqlalchemy

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


def scrape_headline_dataset(url):
    # url = "https://www.bbc.com/news"

    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    headlines = soup.find_all("h2")

    head_list = []
    for x in headlines:
        head_list.append(x.text.strip())
    df = pd.DataFrame({'headline':head_list})
    
    return df 

def data_cleaning(df):

    # remove duplicates
    df_clean = df.copy()
    df_clean = df_clean.drop_duplicates()

    # drop non-headline datasets
    df_clean["count_words"] = df_clean["headline"].str.split().str.len()
    df_clean = df_clean[df_clean["count_words"]> 3]
    df_clean = df_clean.drop(columns = "count_words")

    # Data Cleaning to extract common keywords

    # picks out sequences of alphanumeric characters as tokens
    tokenizer = RegexpTokenizer(r'\w+')
    df_clean["tokens"] = df_clean["headline"].str.lower()
    df_clean["tokens"] = df_clean["tokens"].apply(tokenizer.tokenize)

    # remove stop words
    nltk.download('stopwords')
    stop = stopwords.words('english')
    df_clean["tokens"] = df_clean["tokens"].apply(lambda x: [word for word in x if word not in (stop)])

    # stemming (lemmatize seems to convert us/'US' to u )
    nltk.download('wordnet')
    wordnet = WordNetLemmatizer()
    df_clean["tokens"] = df_clean["tokens"].apply(lambda x: [wordnet.lemmatize(word) for word in x ])
    # ps = PorterStemmer()
    # df_clean["tokens"] = df_clean["tokens"].apply(lambda x: [ps.stem(word) for word in x ])

    df_clean["etl_date"] = pd.to_datetime('today')
    df_clean["etl_date"] = df_clean["etl_date"].dt.normalize()

    return df_clean

def write_postgres(df):

    dtypes = {
        'headline' : sqlalchemy.types.TEXT(),
        'tokens' : sqlalchemy.types.ARRAY(sqlalchemy.types.TEXT()),
        'etl_date' : sqlalchemy.types.DateTime() 
    }

    engine = create_engine('postgresql+psycopg2://postgres:postgres@db_postgres:5432/postgres')
    df.to_sql(name = "bbc", 
              con = engine, 
              index = False,
              dtype = dtypes,
              if_exists = "append")

    engine.dispose()

def main():
    url = "https://www.bbc.com/news"
    df = scrape_headline_dataset(url)
    df_clean = data_cleaning(df)
    write_postgres(df_clean)

if __name__ == '__main__':
    main()