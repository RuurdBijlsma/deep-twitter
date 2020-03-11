from init_db import init_db
from scraper import scrape_tweets_to_db
from prepare_data import get_w2v_model
from network import pre_train_model
from csv_processor import import_csv_to_db
from variables import twitter_user

rebuild_db = False
retrain_w2v = True
retrain_tokenizer = True


def init():
    db, cursor = init_db(clean=rebuild_db)
    if rebuild_db:
        print("Importing csv to database")
        import_csv_to_db(cursor)
        print(f"Scraping data from user {twitter_user}")
        scrape_tweets_to_db(cursor, twitter_user)
        db.commit()
    else:
        print("Using existing database")

    print("Preparing data for neural network")
    w2v_model = get_w2v_model(cursor, retrain_w2v, retrain_tokenizer)
    db.commit()
    print("Training network")
    network = pre_train_model(cursor, w2v_model)
    print(f"Done training {network}")
    # use_network_to_generate_text


if __name__ == '__main__':
    init()
