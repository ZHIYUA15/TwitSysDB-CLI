import pymongo
import sys
import datetime



def search_tweets(db, keywords):
    try:
        # Constructing the query for AND semantics
        query = {"$and": [{"content": {"$regex": f'(?i)\\b{keyword}\\b'}} for keyword in keywords]}
        results = db.tweets.find(query, {"_id": 1, "id": 1, "date": 1, "content": 1, "user.username": 1})
        result_count = db.tweets.count_documents(query)

        if result_count ==0:
            print('No tweets found.')
            return 

        print(f"Searching for tweets with keywords: {keywords}")
        print('')
        tweet_ids = []
        for index, tweet in enumerate(results, 1):
            print('Code: ', index)
            print(f"ID: {tweet['id']}\nDate: {tweet['date']}\nContent: {tweet['content']}\nUsername: {tweet['user']['username']}")
            print('\n')
            tweet_ids.append(tweet['_id'])

        # Ask the user if they want to see more details of a tweet
        if tweet_ids:
            while True:
                tweet_code = input("Enter code of tweet to see more details, or '#' to exit: ")
                if tweet_code == '#':
                    break
                elif tweet_code.isnumeric() and int(tweet_code) in range(1,len(tweet_ids)+1):
                    show_tweet_details(db, tweet_ids[int(tweet_code)-1])
                    break
                else:
                    print('\nWrong input\n')


    except Exception as e:
        print(f"An error occurred in search_tweets: {e}")

def show_tweet_details(db, tweet_id):
    try:
        # Fetching the tweet with all fields based on the ID
        tweet = db.tweets.find_one({"_id": tweet_id})
        if tweet:
            print('\n')
            print("Full details of the tweet:")
            for key, value in tweet.items():
                print(f"{key}: {value}")
        else:
            print("No tweet found with the given ID.")
    except Exception as e:
        print(f"An error occurred in show_tweet_details: {e}")


def list_top_tweets(db):
    try:

        # Ask the user for the field and number of tweets
        field = input("Enter the field to sort by (retweetCount: 1, likeCount: 2, quoteCount: 3): ")
        fields = ['retweetCount', 'likeCount', 'quoteCount']
        if field not in ['1', '2', '3']:
            print("Invalid field. Choose from 1 - retweetCount, 2 - likeCount, 3 - quoteCount.")
            return
        field = fields[int(field) - 1]

        n = int(input("Enter the number of tweets to list: "))

        # Use aggregation pipeline for sorting and limiting the results
        pipeline = [
            {"$project": {"_id": 1, "id": 1, "date": 1, "content": 1, "user.username": 1, field: 1}},
            {"$sort": {field: pymongo.DESCENDING}},
            {"$limit": n}
        ]
        results = db.tweets.aggregate(pipeline)
        tweet_ids= []
        # Display the tweets
        print(f"Top {n} tweets based on {field}:")
        for index, tweet in enumerate(results, 1):
            print('Code:', index)
            print(f"ID: {tweet['id']}\nDate: {tweet['date']}\nContent: {tweet['content']}\nUsername: {tweet['user']['username']}\n{field}: {tweet.get(field, 'N/A')}")
            tweet_ids.append(tweet['_id'])
            print('\n')


        # Ask the user if they want to see more details of a tweet
        if tweet_ids:
            while True:
                tweet_code = input("Enter code of tweet to see more details, or '#' to exit: ")
                if tweet_code == '#':
                    break
                elif tweet_code.isnumeric() and int(tweet_code) in range(1,len(tweet_ids)+1):
                    show_tweet_details(db, tweet_ids[int(tweet_code) - 1])
                    break
                else:
                    print('\nWrong input\n')

    except ValueError:
        print("Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred in list_top_tweets: {e}")


def compose_tweet(db):
    try:
        while True:
            # Ask the user to enter the tweet content
            content = input("Enter your tweet (or enter '#' to exit to the main menu): ")

            # Check for 'exit' command
            if content.lower() == '#':
                print("Exiting to main menu!")
                break

            # Check if the tweet content is not empty
            if content.strip():
                # Create a new tweet document
                new_tweet = {
                    "id": None,
                    "content": content,
                    "date": datetime.datetime.now(),
                    "user": {"username": "291user"},
                    # Setting other fields to null or default values
                }

                # Insert the new tweet into the database
                db.tweets.insert_one(new_tweet)
                print("Your tweet has been posted successfully!")
                break
            else:
                print("Invalid tweet! Please enter some content or enter '#' to exit to the main menu.")

    except Exception as e:
        print(f"An error occurred while composing the tweet: {e}")
