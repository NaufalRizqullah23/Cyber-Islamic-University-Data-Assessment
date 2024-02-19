import asyncio
from twscrape import API
import csv

tw_api = API()

async def add_and_log_into_account():
    await tw_api.pool.add_account("Sinopla23", "Sandalbutut23.", "dajoka23@gmail.com", "Sandalbutut23.")
    await tw_api.pool.login_all()

query = 'cyber islamic university lang:id'
scrapped_tweets = []

async def fetch_tweets(query, limit=10000):
    await add_and_log_into_account()

    counter = 0

    async for tweet in tw_api.search(query):
        tweet_data = {
            "Date": tweet.date,
            "Username": tweet.user.username,
            "Tweet": tweet.rawContent,
        }
        scrapped_tweets.append(tweet_data)

        counter += 1
        if counter >= limit:
            break

asyncio.run(fetch_tweets(query, limit=10000))

csv_file = "CIU_dataset.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Date", "Username", "Tweet"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for tweet_data in scrapped_tweets:
        writer.writerow(tweet_data)

print("Scraped data finished")
