import csv


def import_csv_to_db(cursor, csv_file_name="data/training_tweets.csv"):
    line = 0
    total_tweets = 1600000
    tweet_limit = 50000
    with open(csv_file_name, "rt") as csv_file:
        data_reader = csv.reader(csv_file)
        for [_, _, _, _, user, text] in data_reader:
            line += 1
            cursor.execute('INSERT INTO tweets VALUES(?,?,?)', (None, text, user))
            if line >= tweet_limit:
                print("Hit tweet limit when reading csv")
                break
            if line % 10000 == 0:
                print(f"Tweets processed: [{int(line / 1000)}k / {int(total_tweets / 1000)}k]")
