import pandas as pd
import re
def preprocess(data):
    pattern="\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[A-Z]."
# pattern="\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}"
    date=re.findall(pattern,data)
    date[:5]
    message=re.split(pattern,data)[1:]
    df=pd.DataFrame({"message":message,"message_date":date})
    df["messgae_date"]=pd.to_datetime(df["message_date"],format="%m/%d/%y, %I:%M %p")
    df.rename(columns={"message_date":"date"},inplace=True)
    df.head()

    users=[]
    msg=[]

    for message in df['message']:
        entry=re.split('([\w\W]+?):\s',message)
        
        if entry[1:]:
            x=re.findall(r'[a-zA-Z0-9]+\s*',entry[1])
            
            users.append("".join(x))
            msg.append(entry[2])
        else:
            users.append("Group_notifications")
            msg.append(entry[0])

    df['user']=users
    df['messages']=msg
    df.drop(columns=['message','date'],inplace=True)
    df.head()

    df['year']=df['messgae_date'].dt.year
    df['Month']=df['messgae_date'].dt.month
    df['Month_name']=df['messgae_date'].dt.month_name()
    df['day']=df['messgae_date'].dt.day_name()
    df['hour']=df['messgae_date'].dt.hour
    df['minute']=df['messgae_date'].dt.minute

    #time period
    period=[]

    for hour in df['hour']:
        if hour==23:
            period.append(str(hour)+ '-' + str('00'))
        elif hour==0:
            period.append(str('00')+ '-' + str(hour+1))
        else:
            period.append(str(hour)+ '-' + str(hour+1))
    df['period']=period

    return df