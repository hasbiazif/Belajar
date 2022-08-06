from sre_parse import CATEGORIES
from urllib import response
from googleapiclient.discovery import build
import pandas as pd
from requests import request
import seaborn as sns
import matplotlib.pyplot as plt

api_key = 'xxxxx'
channel_ids = ['UC3J4Q1grz46bdJ7NJLd4DGw', #miawaug
            'UCvh1at6xpV1ytYOAzxmqUsA', #jessnolimit
             'UCVvhlqBpNVoG-DUT3J0oZ-w', #Taraartgame
             'UCXdmo_q4SawYMz-dmeKEHPQ', #dylanpros
             'UCCEs4SbttY3l73m0WsZix3g'] #kemas

youtube = build('youtube', 'v3', developerKey=api_key)

#fungsi untuk mengambil statistik channel

def get_channel_stats(youtube, channel_ids):
    all_data = []

    request = youtube.channels().list(
                part='snippet,contentDetails,statistics',
                id= ','.join(channel_ids)) #pakai join untuk lebih dari 1 channel youtube
    response = request.execute()
    
    for i in range(len(response['items'])): #dilooping untung mengulang lebih dari 1 channel
        data = dict(Channel_name = response['items'] [i] ['snippet']['title'],
                    Subscriber = response['items'][i]['statistics']['subscriberCount'],
                    Views = response['items'][i]['statistics']['viewCount'],
                    Total_Videos = response['items'][i]['statistics']['videoCount'], 
                    playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads']) 
        all_data.append(data)

    return all_data

channel_statistics = get_channel_stats(youtube, channel_ids)

channel_data = pd.DataFrame(channel_statistics)
#print(channel_data)
#print(channel_data.dtypes) #chek tipe datanya

#rubah menjadi int
channel_data['Subscriber'] = pd.to_numeric(channel_data['Subscriber'])
channel_data['Views'] = pd.to_numeric(channel_data['Views'])
channel_data['Total_Videos'] = pd.to_numeric(channel_data['Total_Videos'])
#print(channel_data.dtypes)

#visual
ax = sns.barplot(x='Channel_name', y='Subscriber', data=channel_data)
#plt.show()
#plt.show() #memunculkan plot
#print(channel_data)

#FUNGSI UNTUK MENGAMBIL ID VIDEO
playlist_id = channel_data.loc[channel_data['Channel_name']=='MiawAug', 'playlist_id'].iloc[0]

def get_video_ids(youtube, playlist_id):    #looping untuk mengambil video id dari channel yang disebutkan disini
    
    request = youtube.playlistItems().list(part='contentDetails', playlistId = playlist_id, maxResults = 50)
    response = request.execute()

    video_ids = []

    for i in range(len(response['items'])):         #looping untuk mengambil id dari video channel
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
    
    next_page_token = response.get('nextPageToken')
    more_pages = True

    while more_pages :
        if next_page_token is None :
            more_pages = False
        else :
            request = youtube.playlistItems().list(part='contentDetails', playlistId = playlist_id, maxResults = 50,
                        pageToken = next_page_token)
            for i in range(len(response['items'])):         #looping untuk mengambil id dari video channel
                video_ids.append(response['items'][i]['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')

            response = request.execute()


    return (video_ids)

video_ids = get_video_ids(youtube, playlist_id)
#print(get_video_ids)

#FUNGSI UNTUK MENGAMBIL DETAIL VIDEO

def get_video_details(youtube, video_ids):
    all_videos_stats = []

    for i in range(0, len(video_ids), 50):

        request =youtube.videos().list(
                    part='snippet,statistics',
                    id=','.join(video_ids[i:i+50])) #limit hanya 50
        response = request.execute()

        for video in response['items'] :
            video_stats = dict(Title = video['snippet']['title'],
                                Published_date = video['snippet']['publishedAt'],
                                Views = video['statistics']['viewCount'],
                                Likes = video['statistics']['likeCount']
                                #Dislikes = video['statistics']['dislikeCount'], #youtubesekarang tidak ada dislike
                                #Comments = video['statistics']['commentCount']
                                )
            all_videos_stats.append(video_stats)

    return all_videos_stats
videos_details = get_video_details(youtube, video_ids)
video_data = pd.DataFrame(videos_details)
video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views'] = pd.to_numeric(video_data['Views'])
video_data['Likes'] = pd.to_numeric(video_data['Likes'])
#video_data['Dislikes'] = pd.to_numeric(video_data['Dislikes'])
#video_data['Comments'] = pd.to_numeric(video_data['Comments'])

top10_videos = video_data.sort_values(by='Views', ascending=False).head(10)
#print(top10_videos)
ax1 = sns.barplot(x='Views', y='Title', data=top10_videos)
plt.show()
video_data['Month'] = pd.to_datetime(video_data['Published_date']).dt.strftime('%b')
videos_per_month = video_data.groupby('Month', as_index=False).size()
sort_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Des']
videos_per_month.index = pd.CategoricalIndex(videos_per_month['Month'], categories=sort_order, ordered=True)
videos_per_month = videos_per_month.sort_index()
ax2 = sns.barplot(x='Month', y='size', data=videos_per_month.sort_index())
#plt.show()