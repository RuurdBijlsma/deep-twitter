import csv


def remove_url(tweet):
    parts = tweet.split(' ')
    url_index = -1
    for (i, part) in enumerate(parts):
        if any(tld in part for tld in tlds):
            url_index = i
    if url_index == -1:
        return tweet
    else:
        parts.pop(url_index)
        return ' '.join(parts)


def get_tlds(csv_file_name="data/tlds.csv"):
    with open(csv_file_name, "rt", encoding='utf-8') as csv_file:
        data_reader = csv.reader(csv_file)
        for [tld, _, _] in data_reader:
            yield tld


tlds = list(get_tlds())


def import_csv_to_db(cursor, csv_file_name="data/training_tweets.csv"):
    line = 0
    total_tweets = 1600000
    with open(csv_file_name, "rt") as csv_file:
        data_reader = csv.reader(csv_file)
        for [_, _, _, _, user, text] in data_reader:
            line += 1
            cleaned = remove_url(text)
            cursor.execute('INSERT INTO tweets VALUES(?,?,?,?)', (None, text, cleaned, user))
            if line % 5000 == 0:
                print(f"Tweets processed: [{int(line / 1000)}k / {int(total_tweets / 1000)}k]")
