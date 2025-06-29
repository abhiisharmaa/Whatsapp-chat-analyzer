import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import emoji

def fetch_stats(selected_user, df):
    df = df.dropna()
    if selected_user!= "Group":
        df = df[df["Sender"] == selected_user]

    words = []
    for msg in df["Message"]:
        words.extend(msg.split())

    num_messages = df.shape[0]
    total_media = df[df["Message"].str.contains("video omitted|image omitted", case=False, na=False)].shape[0]
    total_stickers = df[df["Message"]== "sticker omitted"].shape[0]

    return num_messages, len(words),total_media,total_stickers

def most_busy_users(df):
    x = df["Sender"].value_counts().head(5)
    busy_users = round((df["Sender"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={"Sender": "Name", "count":"Baatcheet(%)"})

    return x,busy_users

def words(selected_user, df):
    df = df.dropna()

    if selected_user!= "Group":
        df = df[df["Sender"] == selected_user]
    temp = df[df['Message'] != "video omitted"]
    temp = temp[temp['Message'] != "image omitted"]
    temp = temp[temp['Message'] != "sticker omitted"]
    temp = temp[temp['Sender'] != "group_notification"]
    wc = WordCloud(width=800, height=400, background_color="black")
    df_wc = wc.generate(temp["Message"].str.cat(sep = " "))
    return df_wc


def most_common_words(selected_user, df):
    df = df.dropna()
    if selected_user != "Group":
        df = df[df["Sender"] == selected_user]
    with open("stop_hinglish.txt", "r") as f:
        stop_words = f.read()
    temp = df[df['Message'] != "video omitted"]
    temp = temp[temp['Message'] != "image omitted"]
    temp = temp[temp['Message'] != "sticker omitted"]
    temp = temp[temp['Sender'] != "group_notification"]
    common_words = []
    for msg in temp['Message']:
        for word in msg.lower().split():
            if word not in stop_words:
                common_words.append(word)

    most_common_df =  pd.DataFrame(Counter(common_words).most_common(20),columns=['Word','Frequency'])
    return most_common_df


def common_emojis(selected_user, df):
    df = df.dropna()
    if selected_user!= "Group":
        df = df[df["Sender"] == selected_user]
    emojis = []
    for msg in df['Message'].dropna():
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])

    com_emoji = pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', "Frequency"])
    return com_emoji


def monthly_timeline(selected_user,df):
    if selected_user != 'Group':
        df = df[df['Sender'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['Message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline


def daily_timeline(selected_user,df):
    if selected_user != 'Group':
        df = df[df['Sender'] == selected_user]

    daily_time = df.groupby('only_date').count()['Message'].reset_index()

    return daily_time

def week_activity_map(selected_user,df):

    if selected_user != 'Group':
        df = df[df['Sender'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Group':
        df = df[df['Sender'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Group':
        df = df[df['Sender'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='Message', aggfunc='count').fillna(0)
    return user_heatmap
