import csv


def remove_url(tweet):
    parts = tweet.split(' ')
    url_indices = []
    for (i, part) in enumerate(parts):
        for tld in tlds:
            if tld in part:
                sub_index = part.find(tld)
                next_letter_index = sub_index + len(tld)
                if next_letter_index < len(part):
                    next_letter = part[next_letter_index]
                    if next_letter == '.':
                        continue
                    if next_letter.isalpha():
                        continue
                if sub_index - 1 >= 0:
                    prev_letter = part[sub_index - 1]
                    if not prev_letter.isalpha():
                        continue

                url_indices.append(i)
                break
    if len(url_indices) == 0:
        return tweet
    else:
        for url_index in sorted(url_indices, reverse=True):
            del parts[url_index]
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
            cleaned = cleaned.strip()
            if cleaned != '':
                cursor.execute('INSERT INTO tweets VALUES(?,?,?,?)', (None, text, cleaned, user))
            else:
                print(f"SKIPPED TWEET: {text}")
            if line % 5000 == 0:
                print(f"Tweets processed: [{int(line / 1000)}k / {int(total_tweets / 1000)}k]")
