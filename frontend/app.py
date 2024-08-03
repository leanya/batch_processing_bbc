from ast import literal_eval
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from wordcloud import WordCloud
import psycopg2
from datetime import date
import nltk
from nltk import FreqDist

def form_connection():

    conn = psycopg2.connect(
        database='postgres',
        user='postgres',
        password='postgres',
        host='db_postgres',
        port='5432'
        )
    cursor = conn.cursor()

    return conn, cursor

def extract_dataset(conn, cursor):
    
    sql = "SELECT * FROM bbc"
    cursor.execute(sql)
    query_output = cursor.fetchall()
    # convert to a pandas dataframe 
    df = pd.DataFrame(query_output, columns=['headline', 'tokens', 'etl_date'])

    cursor.close()
    conn.close()

    return df 

def _helper_check_most_freq(x, most_freq_keywords):

    if any(i in most_freq_keywords for i in x):
        return True
    return False

def data_preparation_for_visualisation(df_clean, x_frequent, y_wordcloud):

    # Frequency distribution of all the tokens
    keyword_list = df_clean["tokens"].sum()
    keyword_freqdist = FreqDist(keyword_list) 

    # Extract the top x most frequent keywords 
    most_freq_keywords = []
    for i in keyword_freqdist.most_common(x_frequent):
        most_freq_keywords.append(i[0])
    most_freq_keywords = '|'.join( most_freq_keywords)

    # Extract the corresponding headline of the top 3 most frequent keywords 
    df_headline = df_clean.loc[df_clean.apply(lambda x: _helper_check_most_freq(x['tokens'], most_freq_keywords ), axis = 1), 'headline']
    df_headline = df_headline.reset_index(drop=True)

    # Prepare the string to feed into wordcloud
    keyword_string = ''
    for word, freq in keyword_freqdist.most_common(y_wordcloud):
        inter = ' '.join([word] * freq)
        keyword_string  = keyword_string + inter + ' '
    
    return df_headline, keyword_string 

# Get the dataset 
conn, cursor = form_connection()
df_clean_all = extract_dataset(conn, cursor)
df_clean = df_clean_all.copy()

max_date = df_clean["etl_date"].max()
df_clean = df_clean[df_clean["etl_date"] == max_date]

st.title("News Headline Overview")

y_wordcloud = st.number_input("Insert a number for the wordcloud of the top most frequent keywords", 
                              value = 12)
x_frequent =  st.number_input("Insert a number for the headline of the top most frequent keywords", 
                              value = 3)

df_headline, keyword_string = data_preparation_for_visualisation(df_clean, 
                                                                 x_frequent, 
                                                                 y_wordcloud)

wordcloud = WordCloud().generate(keyword_string)

# Display the wordcloud image:
fig, ax = plt.subplots(figsize = (12, 8))
ax.imshow(wordcloud)
plt.axis('off')
st.pyplot(fig)
st.write("Wordcloud of the top" , y_wordcloud, " most frequent keywords")

st.table(df_headline)
st.write("Headline of the top" , x_frequent, " most frequent keywords")

# streamlit run app.py

