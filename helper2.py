from email import message
from zlib import DEF_BUF_SIZE
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import string
import emoji
import matplotlib.pyplot as plt
import streamlit as st
from urlextract import URLExtract
extract=URLExtract()

def top_user(df):
    top_user=pd.DataFrame(df['user'].value_counts().reset_index() )
    top=top_user['index'][0]
    toppermsg=df[df['user']== top].shape[0]
    total_user=len(df['user'].unique())
    avgmsg=int(df.shape[0]/total_user)
    leftuser=df[df['user']=='Group_message'].shape[0]
    return top,toppermsg,total_user,avgmsg,leftuser

def fetch_Date(selected_user,df):

    start = df.date.min()
    end =  df.date.max()
    difference = end-start
    difference.to_timedelta64()

    average =  df.shape[0]/difference.days

    return start,end,average

def fetch_stats(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    num_messages=df.shape[0]
    word=[]
    num_media_message=df[df['messages']=='<Media omitted>\n'].shape[0]
    for messages in df['messages']:
        word.extend(messages.split())

    links=[]
    for message in df['messages']:
        links.extend(extract.find_urls(message))
    
    num_deleted_message=df[df['messages']=="You deleted this message\n"].shape[0]

    return num_messages,len(word),num_media_message ,len(links),num_deleted_message    

def link(selected_user,df):
    links=[]
    for message in df['messages']:
        links.extend(extract.find_urls(message))
    return links

def topuserdf(df):
    top_userdf=pd.DataFrame(data=df['user'].value_counts().reset_index()  )
    top_userdf.rename(columns={"index":"Name","user":"Total message"},inplace=True)

    return top_userdf
def per_hour_msg(df):
 
    total_hourmsg=pd.DataFrame(df['hour'].value_counts())
    total_hourmsg.reset_index()
    return total_hourmsg



def most_common_words(selected_user,df):
    f=open('hinglish_stopwords.txt','r')
    stop_words=f.read()
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    #remove grp notification
    temp=df[df['user']!='Group_message']
    temp=temp[temp['messages']!="<Media omitted>\n"]

    words=[]

    for message in temp['messages']:
        #remove punctuations 
        new_string = message.translate(str.maketrans('', '', string.punctuation))
        for word in new_string.lower().split():
            if word not in stop_words:
                words.append(word)
    

    most_common_df=pd.DataFrame(Counter(words).most_common(10))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    emojis=[]

    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


    #---------------------
def create_wordcloud(selected_user,df):
    f=open('hinglish_stopwords.txt','r')
    stop_words=f.read()
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    #remove grp notification
    temp=df[df['user']!='Group_notifications']
    temp=temp[temp['messages']!="<Media omitted>\n"]  
    temp=temp[temp['messages']!="You deleted this message\n"]   

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
 
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['messages']=temp['messages'].apply(remove_stop_words)
    df_wc=wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc


def total_messages_month( selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]

    df["months"] =  df["date"].apply(lambda x: x.month_name())

    months_df = df.groupby("months")["messages"].count().sort_values(ascending=False).reset_index()
    perc = [round((i/months_df['messages'].sum()*100),2)  for i in months_df['messages']]
    months_df['percent']= [  (months_df['months'][i] +" = "+ str(perc[i])+"%") if perc[i]>5 else months_df['months'][i] for i in range(months_df.shape[0]) ]   
    return months_df