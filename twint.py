import asyncio
import csv
import twint

async def fetch_tweets(query, limit=10000):
    tweets = []

    c = twint.Config()
    c.Search = query
    c.Limit = limit
    c.Store_object = True
    c.Store_object_tweets_list = tweets

    await twint.run.Search(c)

    return tweets

async def main():
    query = 'cyber islamic university lang:id'
    limit = 10000

    tweets = await fetch_tweets(query, limit)

    csv_file = "CIU_datset.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["date", "username", "tweet"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for tweet in tweets:
            writer.writerow({
                "date": tweet.datestamp,
                "username": tweet.username,
                "tweet": tweet.tweet
            })

if __name__ == "__main__":
    asyncio.run(main())
