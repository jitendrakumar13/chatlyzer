from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import string
import emoji

from urlextract import URLExtract
extract=URLExtract()
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

    return num_messages,len(word),num_media_message ,len(links)    


def fetch_busy_user(df):

    x=df['user'].value_counts().head()
    df1=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})

    return x,df1

def create_wordcloud(selected_user,df):
    f=open('hinglish_stopwords.txt','r')
    stop_words=f.read()
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    #remove grp notification
    temp=df[df['user']!='Group_notifications']
    temp=temp[temp['messages']!="<Media omitted>\n"]   

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



def most_common_words(selected_user,df):
    f=open('hinglish_stopwords.txt','r')
    stop_words=f.read()
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    #remove grp notification
    temp=df[df['user']!='Group_notifications']
    temp=temp[temp['messages']!="<Media omitted>\n"]

    words=[]

    for message in temp['messages']:
        #remove punctuations 
        new_string = message.translate(str.maketrans('', '', string.punctuation))
        for word in new_string.lower().split():
            if word not in stop_words:
                words.append(word)
    

    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    emojis=[]

    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
    
def monthly_timeline(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]   

    timeline=df.groupby(['year','Month_name','Month']).count()['messages'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append( (timeline['Month_name'][i]) + "-" + str(timeline['year'][i])  )
    
    timeline['time']=time

    return timeline

def activity_week_map(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    
    return df['day'].value_counts()

def activity_month_map(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    
    return df['Month_name'].value_counts()
 
def activity_heatmap(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    activity=df.pivot_table(index='day',columns='period',values='messages',aggfunc='count').fillna(0)

    return activity
 
