import pymongo
import sys
import datetime


def search_users(db,keyword):
    try:

        regex_keyword = f'(?i)\\b{keyword}\\b'
        # Query to find users based on the keyword
        query = {
            "$or": [
                {"user.displayname": {"$regex": regex_keyword, "$options": "i"}},
                {"user.location": {"$regex": regex_keyword, "$options": "i"}}
            ]
        }
        projection = {"user.username": 1, "user.displayname": 1, "user.location": 1}
        results = db.tweets.find(query, projection)
        result_count = db.tweets.count_documents(query)

        if result_count == 0:
            print('No users found')
            return
        
        # Display the users
        print(f"Users matching keyword '{keyword}':")
        unique_users = set()
        user_ids = []
        counter = 1
        print('\n')
        for tweet in results:
            user = tweet.get('user',{})
            username = user.get('username', 'N/A')

            if username not in unique_users:
                unique_users.add(username)
                print('Code: ', counter)
                print(f"Username: {username}\nDisplayname: {user.get('displayname', 'N/A')}\nLocation: {user.get('location', 'N/A')}\n")
                user_ids.append(user['username'])
                counter+=1

        # Ask the user if they want to see more details of a user
        if user_ids:
            valid = False
            while not valid:
                user_id = input("Enter code to see more details, or '#' to exit: ")
                if user_id.isnumeric() and int(user_id) in range(1, len(user_ids)+1):
                    show_user_details(db, user_ids[int(user_id)-1])
                    valid = True
                elif user_id.lower() == '#':
                    valid = True
                else:
                    print('Wrong input')
                


    except Exception as e:
        print(f"An error occurred in search_users: {e}")

def show_user_details(db, username):
    try:
        # Fetching the user with all fields based on the username
        user = db.tweets.find_one({"user.username": username}, {"user": 1})
        if user and "user" in user:
            print("Full details of the user:")
            for key, value in user["user"].items():
                print(f"{key}: {value}")
        else:
            print("No user found with the given username.")
    except Exception as e:
        print(f"An error occurred in show_user_details: {e}")

def list_top_users(db):
    try:
        # Ask the user for the number of users to list
        n = int(input("Enter the number of users to list: "))

        # Aggregation query to find top users based on followersCount
        pipeline = [
            {"$group": {
                "_id": "$user.username",
                "displayname": {"$first": "$user.displayname"},
                "followersCount": {"$first": "$user.followersCount"}
            }},
            {"$sort": {"followersCount": -1}},
            {"$limit": n}
        ]
        results = db.tweets.aggregate(pipeline)

        # Display the users
        print(f"Top {n} users based on followersCount: \n")
        user_ids = []

        for index, user in enumerate(results,1):
            print('Code: ', index)
            print(f"Username: {user['_id']}\nDisplayname: {user['displayname']}\nFollowers Count: {user['followersCount']}")
            print('\n')
            user_ids.append(user['_id'])

        # Ask the user if they want to see more details of a user
        if user_ids:
            valid = False
            while not valid:
                user_id = input("Enter code to see more details, or '#' to exit: ")
                if user_id.isnumeric() and int(user_id) in range(1, len(user_ids)+1):
                    show_user_details(db, user_ids[int(user_id)-1])
                    valid = True
                elif user_id.lower() == '#':
                    valid = True
                else:
                    print('Wrong input')

    except ValueError:
        print("Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred in list_top_users: {e}")