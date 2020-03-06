from init_db import init_db
from scraper import user_tweets_to_db
from prepare_data import prepare_data
from network import train_network


scrape = False
user = "BarackObama"


def init():
    db, cursor = init_db()
    if scrape:
        print(f"Scraping data from user {user}")
        user_tweets_to_db(cursor, user, 4)
    else:
        print("Skipping scrape")
    print("Preparing data for neural network")
    input_sequence, output_sequence = prepare_data(cursor)
    print("Training network")
    network = train_network(input_sequence, output_sequence)
    print(f"Done training {network}")
    # use_network_to_generate_text


if __name__ == '__main__':
    init()
