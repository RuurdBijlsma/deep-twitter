from twitterscraper import query_tweets

if __name__ == '__main__':
    # Or save the retrieved tweets to file:
    file = open("out/output.txt", "w")
    for tweet in query_tweets("Trump OR Clinton", 10):
        print(tweet.encode('utf-8'))
        file.write(tweet.encode('utf-8'))
    file.close()
