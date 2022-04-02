import pandas as pd
import re
def process(data):
    pattern="\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[A-Z]."
    message=re.split(pattern,data)[1:]
    date=re.findall(pattern,data)
    df=pd.DataFrame({"message":message,"message_date":date})
    df["messgae_date"]=pd.to_datetime(df["message_date"],format="%m/%d/%y, %I:%M %p")
    df.rename(columns={"message_date":"date"},inplace=True)
    users=[]
    msg=[]

    for message in df['message']:
        entry=re.split('([\w\W]+?):\s',message)
        
        if entry[1:]:
            x=re.findall(r'[a-zA-Z0-9]+\s*',entry[1])
            
            users.append("".join(x))
            if(len(entry[2])==0):
                msg.append("No message")
            else:
                msg.append(entry[2])
        else:
            users.append("Group_message")
            if(len(entry[0])==0):
                msg.append("No message")
            else:
                msg.append(entry[0])
    df['user']=users
    df['messages']=msg
    df.drop(columns=['message','date'],inplace=True)
 

    df['year']=df['messgae_date'].dt.year
    df['month']=df['messgae_date'].dt.month
    df['month_name']=df['messgae_date'].dt.month_name()
    df['day']=df['messgae_date'].dt.day_name()
    df['hour']=df['messgae_date'].dt.hour
    df['minute']=df['messgae_date'].dt.minute
    x=df.copy()
    x['time']=x['messgae_date'].dt.time
    def f(x):
        if (x > 4) and (x <= 8):
            return 'Early Morning'
        elif (x > 8) and (x <= 12 ):
            return 'Morning'
        elif (x > 12) and (x <= 16):
            return'Noon'
        elif (x > 16) and (x <= 20) :
            return 'Eve'
        elif (x > 20) and (x <= 24):
            return'Night'
        elif (x <= 4):
            return'Late Night'
    df['part_of_day']=df['hour'].apply(f)
    df['day']=df['day'].str[:3]
    df.rename(columns={"messgae_date":"date"},inplace=True)
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
