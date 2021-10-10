import urllib
from requests_oauthlib import OAuth1
import requests
from datetime import datetime, timedelta
import pandas as pd
import pytz
import openpyxl
import environ

timezone = pytz.timezone('Asia/Tokyo')
ts = datetime.now(tz=timezone)
until_ts = ts  + timedelta(weeks=-1)
until = '{0:%Y-%m-%d}'.format(until_ts)

env = environ.Env()
env.read_env('.env')

def main():
    # APIKEY
    CONSUMER_KEY = env("CONSUMER_KEY")
    CONSUMER_SECRET = env("CONSUMER_SECRET")
    ACCESS_TOKEN = env("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = env("ACCESS_TOKEN_SECRET")


    # paramater
    word = "ハンドソープ"
    count = 100
    search_range = 1#80
    tweets = search_tweets(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, word, count, search_range)
    result_df = pd.DataFrame(
                              tweets,
                              index=None,
                              columns=['TweetID',
                                      'PostedTime',
                                      'UserName',
                                      'UserID',
                                      'UserScreenName',
                                      'UserFavourites',
                                      'UserFollowers',
                                      'UserFriends',
                                      'PostRetweet',
                                      'PostFavorite',
                                      'PostMessage'])

def search_tweets(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, word, count, search_range):
    word = urllib.parse.quote_plus(word)
    url = "https://api.twitter.com/1.1/search/tweets.json?lang=ja&q="+word+"&count="+str(count)
    auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    response = requests.get(url, auth=auth)
    data = response.json()['statuses']

    cnt = 0
    num_of_tweet = 0
    tweets = []
    while True:
        if len(data) == 0:
            break
        cnt += 1
        if cnt > search_range:
            break
        for tweet in data:
            tweets.append([
                          tweet['id_str'],                                   # ツイートID
                          '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S %z %Y") + timedelta(hours=9)),          # 投稿日
                          tweet['user']['name'],                                # ユーザー名
                          tweet['user']['id_str'],                              # ユーザーID
                          tweet['user']['screen_name'],                         # ユーザー表示名
                          tweet['user']['favourites_count'],                    # ユーザーお気に入り数
                          tweet['user']['followers_count'],                     # フォロワー数
                          tweet['user']['friends_count'],                       # フレンド数
                          tweet['retweet_count'],                            # リツイート数
                          tweet['favorite_count'],                           # 投稿お気に入り数
                          tweet['text']                                      # 投稿文
              ])
            maxid = int(tweet["id"]) - 1
        url = "https://api.twitter.com/1.1/search/tweets.json?lang=ja&q="+word+"&count="+str(count)+"&max_id="+str(maxid)
        response = requests.get(url, auth=auth)
        num_of_tweet += 1
        try:
            data = response.json()['statuses']
        except KeyError:
            break
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = 'tweet_data'

    sheet["A1"].value = "tweetID"
    sheet["B1"].value = "投稿日"
    sheet["C1"].value = "ユーザー名"
    sheet["D1"].value = "ユーザーID"
    sheet["E1"].value = "ユーザー表示名"
    sheet["F1"].value = "ユーザー表示名"
    sheet["G1"].value = "ユーザーお気に入り数"
    sheet["H1"].value = "フォロー数"
    sheet["I1"].value = "フレンド数"
    sheet["J1"].value = "リツイート数"
    sheet["K1"].value = "投稿お気に入り数"
    sheet["L1"].value = "投稿文"
    #計12項目

    i = 1
    n = 1
    for tweet in tweets:
      print(tweet)
      while 13 > n:
        sheet.cell(column=n,row=i+1,value=tweet[n-1])
        n += 1
      n = 1
      i += 1
      if i > num_of_tweet:
        break
    wb.save('tweet.xlsx')

if __name__ == '__main__':
  main()
