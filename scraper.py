from twitterscraper import query_tweets_from_user
from csv_processor import remove_url


def scrape_tweets_to_db(cursor, user, limit=None):
    for tweet in query_tweets_from_user(user, limit=limit):
        cursor.execute('''INSERT INTO tweets VALUES(?,?,?,?)''',
                       (None, tweet.text, remove_url(tweet.text), tweet.screen_name))
