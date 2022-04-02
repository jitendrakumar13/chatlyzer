from distutils.command.upload import upload
from json import tool
import matplotlib
from numpy import average
import seaborn as sns
 
import squarify
import streamlit as st
import matplotlib.pyplot as plt
import preprocess2,helper2
st.set_page_config(layout="wide")
st.markdown("This project is created by jitendra kumar ")
st.markdown(" you can visit my Linkedin Profile [link](https://www.linkedin.com/in/jeetu182370/) and also the github profile [link](https://github.com/jitendrakumar13) )")
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocess2.process(data)
    # st.dataframe(df)
    
    #fetch unique users 
    st.header("Whatsapp Chat Analyzer 📊 ")

    user_list=df['user'].unique().tolist()
    user_list.remove('Group_message')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show analysis",user_list)
    if st.sidebar.button("Show analysis"):
        start,end,average=helper2.fetch_Date(selected_user,df)
        st.subheader( 'Your uploded file contains chats from ' + str(start.date())+' to '+str(end.date()))
        st.title(selected_user)
        st.dataframe(df)


    #contents
#---------------------------------------

        num_messages,words,num_media_message,num_links,deleted_msg=helper2.fetch_stats(selected_user,df)
        col1,col2,col3,col4,col5=st.columns(5)

        with col1:
            st.subheader("Total Messages")
            st.markdown(num_messages)
        with col2:
            st.subheader("Total Words")
            st.markdown(words)
        with col3:
            st.subheader("Media Shared")
            st.markdown(num_media_message)
        with col4:
            st.subheader("Links Shared")
            st.markdown(num_links)
        with col5:
            st.subheader("Total Deleted Message")
            st.markdown(deleted_msg)
            
#---------------------------------------

#top_user
#------------------------------
    top,toppermsg,total_user,avgmsg,leftuser=helper2.top_user(df)
    col1,col2,col3,col4=st.columns(4)

    with col1:
        st.subheader("Top User")
        st.markdown(top)
        st.markdown(toppermsg)
    with col2:
        st.subheader("Average message")
        st.markdown(avgmsg)
    with col3:
        st.subheader("Total User")
        st.markdown(total_user)
    with col4:
        st.subheader("Left/Add")
        st.markdown(leftuser)

    col1,col2=st.columns([3,1])
    topuserdf=helper2.topuserdf(df)
    with col1:
        st.markdown("All Memebers..")
        fig,ax=plt.subplots(figsize=(10,5))
        ax.bar(topuserdf['Name'],topuserdf['Total message'])
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        plt.show()
        st.pyplot(fig)
    with col2:
        st.markdown("Top 10 users...")
        st.dataframe(topuserdf.head(10))



#countplot per user 
    col1,col2 =st.columns([1,3])
    with col1:
        st.markdown("Total Messages")
        st.dataframe(df['part_of_day'].value_counts())

    with col2:
        st.subheader("Busiest Part of the day...")
        sns.countplot(df['part_of_day'])
        plt.tight_layout()
        plt.show()
        st.pyplot(fig)



    st.subheader("24 hour time data Analysis...")
    fig = plt.figure(figsize =(10,5))
    sns.countplot(df['hour'],hue=df['part_of_day'])
    plt.tight_layout()
    plt.show()
    st.pyplot(fig)

    total_hourmsg=helper2.per_hour_msg(df)
    fig = plt.figure(figsize =(10,5))
    plt.bar(total_hourmsg.index,total_hourmsg['hour'])
    plt.tight_layout()
    plt.show()
    st.pyplot(fig)


    st.subheader("Overall Analysis according to 24hr time with year ")
    fig = plt.figure(figsize =(10,5))
    g=sns.countplot(df['hour'],hue=df['year'])
    sns.move_legend(g, "upper right", title='Year')
    plt.tight_layout()
    plt.show()
    st.pyplot(fig)


    st.subheader("Most Common Words")
    most_common_df=helper2.most_common_words(selected_user,df)
    fig,ax=plt.subplots()
    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation='vertical')

    st.pyplot(fig)


    #emoji analysis
    st.subheader("Emoji Analysis")
    emoji_df=helper2.emoji_helper(selected_user,df)
    st.title("Emoji Analysis")
    col1,col2=st.columns(2)

    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig,ax=plt.subplots()
        ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
        st.pyplot(fig)
        
            #wordcloud    
        
    st.markdown("WordCloud")
    df_wc=helper2.create_wordcloud(selected_user,df)
    fig,ax=plt.subplots(figsize =(10,5))
    ax.imshow(df_wc)
    st.pyplot(fig)

#per month bar graph 

    st.subheader("Monthly Analysis")
    monthly= helper2.total_messages_month(selected_user,df)
    fig = plt.figure(figsize =(10,5))
    plt.bar(monthly.months,monthly.messages)
    plt.tight_layout()
    plt.show()
    st.pyplot(fig)


    #treemap
    st.subheader("TreeMap")
    treemap= helper2.total_messages_month(selected_user,df)
    #matplotlib.rcParams.update({'font.size': 8})
    fig,ax=plt.subplots(figsize =(10,5))
    # plt.style.use('ggplot')
    ax=squarify.plot(sizes=treemap['messages'], label= treemap['percent'], alpha=.6,pad=True,text_kwargs={'fontsize':6}  )
    plt.tight_layout()
    plt.axis('off')
    st.pyplot(fig)

#total url shared :
    col1,col2=st.columns(2)
    with col1:
        links_=helper2.link(selected_user,df)
        st.subheader("Total shared url links..")
        st.dataframe(links_)
 
