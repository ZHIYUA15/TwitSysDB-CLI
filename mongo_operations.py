import pymongo
import sys
import time
import datetime
from tweets_operations import *
from users_operations import *

def connect_to_mongo(port):
    client = pymongo.MongoClient(f"mongodb://localhost:{port}/")
    db = client["291db"]
    return db



def main_menu(db):
    while True:
        time.sleep(1) # Slight delay for better readability of the menu
        print('\n\n')
        print("##################")
        print("**Main Menu**")
        print("1. Search for Tweets")
        print("2. Search for Users")
        print("3. List Top Tweets")
        print("4. List Top Users")
        print("5. Compose a Tweet")
        print("6. Exit")
        print("##################")
        choice = input("Enter your choice: ").strip() # Get the user's choice

        if choice == "1":
            # Search for tweets based on user-entered keywords
            keywords = input("Enter keywords (separated by space): ").strip().split()
            valid = True
            if not keywords:
                print('Wrong input')
                valid = False
            if valid: 
                search_tweets(db,keywords)

        elif choice == "2":
            # Search for users based on a user-entered keyword
            keyword = input("Enter a keyword for User search: ").strip()
            if len(keyword) < 1:
                print('Wrong input')
            else:
                search_users(db, keyword)

        elif choice == "3":
            # List top tweets based on user-selected criteria
            list_top_tweets(db)

        elif choice == "4":
            # List top users based on user-selected criteria
            list_top_users(db)

        elif choice == "5":
            # Allow the user to compose and post a tweet
            compose_tweet(db)

        elif choice == "6":
            # Exit the program
            break

        else:
            # Handle invalid input
            print('Wrong input')

if __name__ == "__main__":
    # Ensure correct usage with the required command-line argument
    if len(sys.argv) != 2:
        print("Usage: mongo_operations.py <mongo_port>")
        sys.exit(1)

    # Connect to MongoDB and launch the main menu
    mongo_port = sys.argv[1]
    db = connect_to_mongo(mongo_port)
    main_menu(db)