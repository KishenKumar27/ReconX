import pymongo

async def save_sentiment(sentiment_data: dict, mongodb_client: pymongo.MongoClient):
    """Save sentiment data to MongoDB."""
    mydb = mongodb_client["sentiment"]
    mycol = mydb["forex"]

    filter = {
        "name": sentiment_data["name"]
    }

    mycol.update_one(
        filter=filter,
        update={ "$set": sentiment_data },
        upsert=True
    )