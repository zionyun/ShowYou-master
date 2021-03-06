import requests
from bs4 import BeautifulSoup
import datetime
import time
import GetOldTweets3 as got
from random import uniform
from tqdm import tqdm
import pandas as pd

import pymongo
from . import mongo_connection

def parsing(keyword,day):

    days_range = []
    num = 0

    if day == 'm':
        num = 30


    elif day == 'd':
        num = 1


    elif day == 'w':
        num = 7

    end = datetime.date.today()
    start = end - datetime.timedelta(days=num)
    print(end)

    end = end.strftime("%Y-%m-%d")
    start = start.strftime("%Y-%m-%d")

    start = datetime.datetime.strptime(start,"%Y-%m-%d")
    end = datetime.datetime.strptime(end,"%Y-%m-%d")

    date_generated = [start + datetime.timedelta(days=x) for x in range(0,(end-start).days)]

    for date in date_generated:
        days_range.append(date.strftime("%Y-%m-%d"))

    # print("=== 설정된 트윗 수집 기간은 {} 에서 {} 까지 입니다 ===".format(days_range[0], days_range[-1]))
    # print(keyword)
    print("=== 총 {}일 간의 데이터 수집 ===".format(len(days_range)))


    # 수집 기간 맞추기
    start_date = days_range[0]
    end_date =(datetime.datetime.strptime(days_range[-1], "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")# setUntil이 끝을 포함하지 않으므로, day + 1

    # 트윗 수집 기준 정의 // 원하는 검색어 설정하기 
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword).setSince(start_date).setUntil(end_date).setMaxTweets(100).setEmoji("unicode")

    # 수집 with GetOldTweet3
    print("Collecting data start.. from {} to {}".format(days_range[0], days_range[-1]))
    start_time = time.time()
    
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)
   
    print("Collecting data end.. {0:0.2f} Minutes".format((time.time() - start_time)/60))
    print("=== Total num of tweets is {} ===".format(len(tweet)))

    tweet_list = []
        
    i = 0
    for index in tqdm(tweet):
        # 메타데이터 목록 
        username = index.username 
        content = index.text
        # 결과 합치기
        info_list = {}
        info_list['post_id'] = i
        info_list['person_id'] = username
        info_list['post'] = content
        tweet_list += [info_list]
        i = i + 1
    
    mongo_connection.post_insert(tweet_list)

    twitter_df = pd.DataFrame(tweet_list, columns = ["user_name", "text"])

    # csv 파일 만들기
    # twitter_df.to_csv("{}_twitter_data_{}_to_{}.csv".format(keyword,days_range[0], days_range[-1]), index=False)
    # print("=== {} tweets are successfully saved ===".format(len(tweet_list)))
    # df_tweet = pd.read_csv('{}_twitter_data_{}_to_{}.csv'.format(keyword,days_range[0], days_range[-1]))
    # df_tweet.head(10)

# parsing('네일아트','m')