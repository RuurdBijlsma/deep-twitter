from twitterscraper import query_tweets, query_tweets_from_user, query_user_info


def user_tweets_to_db(cursor, user, limit=5):
    for tweet in query_tweets_from_user(user, limit=limit):
        cursor.execute('''INSERT INTO tweets VALUES(?,?,?)''', (None, tweet.text, tweet.screen_name))
