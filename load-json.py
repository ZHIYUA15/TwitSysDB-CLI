import json
import pymongo
import sys

def connect_to_mongo(port):
    client = pymongo.MongoClient(f"mongodb://localhost:{port}/")
    db = client["291db"]
    return db

def load_json_to_mongodb(json_file, db):
    collection = db["tweets"]
    try:
        collection.drop()  # Drop the collection if it exists
        print("Existing 'tweets' collection dropped.")

        # Load the JSON data into the collection
        with open(json_file, 'r') as file:
            batch = []
            batch_size = 1000  # Adjust batch size as needed
            for line in file:
                tweet = json.loads(line)
                batch.append(tweet)
                if len(batch) == batch_size:
                    collection.insert_many(batch)
                    batch = []
            if batch:  # Insert any remaining tweets
                collection.insert_many(batch)
        print(f"Data from {json_file} successfully loaded into MongoDB.")

        # Create indexes on the specified fields
        collection.create_index([("retweetCount", pymongo.DESCENDING)])
        collection.create_index([("likeCount", pymongo.DESCENDING)])
        collection.create_index([("quoteCount", pymongo.DESCENDING)])
        collection.create_index([("user.displayname", pymongo.ASCENDING)])
        collection.create_index([("user.location", pymongo.ASCENDING)])
        collection.create_index([("user.followersCount", pymongo.DESCENDING)])

        print("Indexes created on retweetCount, likeCount, quoteCount, displayname, location, and followersCount.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: load-json.py <json_file> <mongo_port>")
        sys.exit(1)

    json_file = sys.argv[1]
    mongo_port = sys.argv[2]

    db = connect_to_mongo(mongo_port)
    load_json_to_mongodb(json_file, db)
