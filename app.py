from flask import Flask
from flask import render_template, redirect, url_for, request
import os
import openai
import requests
import json
import random
import pandas as pd
from datetime import datetime
from database_interface import print_all_entries
from database_interface import close_database_connection
from database_interface import query_database
from database_interface import print_query_retrieval
from database_interface import create_sqlite_db
from bar_interface import make_bar
from openai import OpenAI


#api_key = '8YQ53Ao5sqOGEq826OfsK3PqOEQBWY36Iv0KJsTx'
api_key = 'VdOqVd04mWYqEU46GwwclqlBTq3pZpvkZgjOv3m7'
base_url = 'https://api.watchmode.com/v1/title/'
gpt_api = ""
api_key_extra = 'c4f00ce17c0faa40f53c4be57abbc890'

csv_file = 'title_id_map.csv'
db_file = 'movies.db'

# reviews = dict()

def get_now_playing_movies(api_key):
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}&region=US"
    base_image_url = "https://image.tmdb.org/t/p/w500"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        
        movies = []
        
        for movie in results:
            movie_info = {
                'overview': movie.get('overview'),
                'original_title': movie.get('original_title'),
                'poster_path': base_image_url + movie.get('poster_path') if movie.get('poster_path') else None,
                'release_date': movie.get('release_date'),
                'original_language': movie.get('original_language')
            }
            movies.append(movie_info)
        
        return movies
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return None

def get_current_date():
    return datetime.now().strftime("%m/%d/%Y")

def convert_backslashes_to_slashes(path_str):
    # Replace all instances of backslashes with forward slashes
    return path_str.replace('\\', '/')


def convert_date(date_str):
    # Convert the string to a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    
    # Format the datetime object to the desired format
    formatted_date = date_obj.strftime("%B %d")
    
    # Return the formatted date string
    return formatted_date

def convert_current_date(date_str):
    # Convert the string to a datetime object
    date_obj = datetime.strptime(date_str, "%m/%d/%Y")
    
    # Extract the day of the month and determine the appropriate suffix
    day = date_obj.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    
    # Format the datetime object to the desired format
    formatted_date = date_obj.strftime(f"%B {day}{suffix}, %Y")
    
    # Return the formatted date string
    return formatted_date

active_user = dict()

users = {
    1: {
        "id" : 1,
        "username" : "asder4215",
        "profile_picture" : "https://cdn.myanimelist.net/s/common/userimages/dd32b9ac-4642-4743-936f-c551486b3396_225w?s=952a217493e230e0141e16d4c1fe5be7",
        "currently_watching": ["Inception", "The Matrix", "Oppenheimer"],
        "completed" : 1, # 1
        "watching" : 2, # 3
        "on_hold" : 8, # 5
        "status" : "On vacation",
        "bio" : "Diving deep into captivating storylines, thrilling adventures, and fantastical worlds across various genres, from superhero blockbusters to chilling horror tales, epic sci-fi sagas, and stunning animated masterpieces. Always on the lookout for my next great watch, I enjoy delving into diverse narratives and discussing the intricacies of storytelling. Let's geek out over our favorite shows and movies together!",
        "joined" : "June 6th, 2023",
        "birthdate" : "December 27",
        "gender" : "Male",
        "movies" : {
            "The Batman": (1532981, "Watching"),
            "The Dark Knight" : (1386160, "Completed"),
            "Batman Begins" : (144341, "On Hold")
        },
        "series" : {
            "Spider-Man: No Way Home": (1589918, "Watching"),
            "Spider-Man: Far From Home" : (1357314, "Completed"),
            "Spider-Man: Homecoming" : (1357316, "On Hold")
        },
        "recent" : [
            1196323,
            1472956,
            1129894
        ],
        "friends" : [
            2,
            3,
            4
        ],
        "reviews" : [
            
        ]
    },
    2: {
        "id" : 2,
        "username" : "Tym",
        "profile_picture" : "https://cdn.myanimelist.net/s/common/userimages/1c7aaac1-c45e-4d57-86a9-ce9d6a3da39c_225w?s=8559a9ceb409980b72e605a9b4c69e11",
        "currently_watching": ["Inception", "The Matrix", "Oppenheimer"],
        "completed" : 1, # 1
        "watching" : 2, # 3
        "on_hold" : 8, # 5
        "status" : "In class",
        "bio" : "Immersed in the magic of storytelling, I explore a myriad of genres from action-packed superhero epics to spine-tingling horror flicks, imaginative sci-fi odysseys, and heartwarming animated features. Constantly hunting for my next cinematic adventure, I revel in dissecting narratives and uncovering hidden gems. Let's bond over our mutual love for movies and TV shows, sharing our favorites and debating the latest plot twists!",
        "joined" : "January 8th, 2022",
        "birthdate" : "March 25",
        "gender" : "Male",
        "movies" : {
            "Inception": (1182444, "Completed"),
            "Fight Club" : (1406847, "Completed"),
            "The Matrix" : (1132806, "Completed"),
            "The Social Network": (1419997, "Completed"),
            "The Dark Knight" : (1386160, "Completed")
        },
        "series" : {
            "Blade Runner 2049": (153801, "Watching"),
            "War for the Planet of the Apes" : (1357314, "Watching"),
            "Logan" : (1461946, "On Hold")
        },
        "recent" : [
            1182444,
            1406847,
            1132806
        ],
        "friends" : [
            1,
            3,
            4
        ],
        "reviews" : [
            1386160,
            1419997
        ]
    },
    3: {
        "id" : 3,
        "username" : "dankskillz",
        "profile_picture" : "https://cdn.myanimelist.net/s/common/userimages/3484be0c-3ae4-4411-ac04-2c686f92a51b_225w?s=531ad7cf9332297283e4ff09e23dad2d",
        "currently_watching": ["Inception", "The Matrix", "Oppenheimer"],
        "completed" : 1, # 1
        "watching" : 2, # 3
        "on_hold" : 8, # 5
        "status" : "At work",
        "bio" : "A connoisseur of diverse narratives, I journey through an array of genres including thrilling action, eerie horror, expansive sci-fi, and enchanting animated tales. Ever in search of the next gripping story, I cherish analyzing plot intricacies and character arcs. Let's connect over our passion for the screen, exchanging recommendations and diving deep into our favorite films and series!",
        "joined" : "April 10th, 2021",
        "birthdate" : "August 19",
        "gender" : "Male",
        "movies" : {
            "The Bourne Ultimatum": (1381053, "Completed"),
            "Avatar" : (138014, "Completed"),
            "The Martian" : (1406622, "Completed"),
            "The Dark Knight" : (1386160, "Completed")
        },
        "series" : {
            "Star Wars: The Force Awakens": (1359306, "Watching"),
            "Thor: Ragnarok" : (1431650, "On Hold"),
            "Stargate Universe" : (3102379, "On Hold")
        },
        "recent" : [
            1381053,
            138014,
            1406622
        ],
        "friends" : [
            2,
            1,
            4
        ],
        "reviews" : [
            1386160
        ]
    },
    4: {
        "id" : 4,
        "username" : "g4v1ng72",
        "profile_picture" : "https://cdn.myanimelist.net/s/common/userimages/c21b7e17-a3d8-4e23-b70b-6f655903030e_225w?s=6e46e9233497e7c04f40d371dfd4e11a",
        "currently_watching": ["Inception", "The Matrix", "Oppenheimer"],
        "completed" : 1, # 1
        "watching" : 2, # 3
        "on_hold" : 8, # 5
        "status" : "Vibing",
        "bio" : "Captivated by the art of storytelling, I delve into genres ranging from adrenaline-fueled superhero sagas to bone-chilling horror, vast sci-fi realms, and delightful animated adventures. Always eager for my next viewing experience, I love discussing the layers and details of different narratives. Join me in celebrating our shared enthusiasm for movies and TV shows, and let's explore the cinematic world together!",
        "joined" : "May 17th, 2020",
        "birthdate" : "September 21",
        "gender" : "Male",
        "movies" : {
            "The Social Network": (1419997, "Completed"),
            "Saving Private Ryan" : (1334825, "Completed"),
            "Schindler's List" : (1335706, "Completed")
        },
        "series" : {
            "Titanic": (1434734, "On Hold"),
            "Casablanca" : (168295, "On Hold"),
            "Die Hard" : (1102562, "On Hold")
        },
        "recent" : [
            1419997,
            1334825,
            1335706
        ],
        "friends" : [
            2,
            3,
            1
        ]
    }
}

users_names = {
    "asder4215": {
        "id" : 1,
        "username" : "asder4215",
        "profile_picture" : "https://cdn.myanimelist.net/s/common/userimages/dd32b9ac-4642-4743-936f-c551486b3396_225w?s=952a217493e230e0141e16d4c1fe5be7",
        "currently_watching": ["Inception", "The Matrix", "Oppenheimer"],
        "completed" : 1, # 1
        "watching" : 2, # 3
        "on_hold" : 8, # 5
        "status" : "On vacation",
        "bio" : "Diving deep into captivating storylines, thrilling adventures, and fantastical worlds across various genres, from superhero blockbusters to chilling horror tales, epic sci-fi sagas, and stunning animated masterpieces. Always on the lookout for my next great watch, I enjoy delving into diverse narratives and discussing the intricacies of storytelling. Let's geek out over our favorite shows and movies together!",
        "joined" : "June 6th, 2023",
        "birthdate" : "December 27",
        "gender" : "Male",
        "movies" : {
            "The Batman": (1532981, "Watching"),
            "The Dark Knight" : (1386160, "Completed"),
            "Batman Begins" : (144341, "On Hold")
        },
        "series" : {
            "Spider-Man: No Way Home": (1589918, "Watching"),
            "Spider-Man: Far From Home" : (1357314, "Completed"),
            "Spider-Man: Homecoming" : (1357316, "On Hold")
        },
        "recent" : [
            1196323,
            1472956,
            1129894
        ],
        "friends" : [
            2,
            3,
            4
        ],
        "reviews" : [
            
        ]
    },
    "Tym": {
        "id" : 2,
        "username" : "Tym",
        "profile_picture" : "https://cdn.myanimelist.net/s/common/userimages/1c7aaac1-c45e-4d57-86a9-ce9d6a3da39c_225w?s=8559a9ceb409980b72e605a9b4c69e11",
        "currently_watching": ["Inception", "The Matrix", "Oppenheimer"],
        "completed" : 1, # 1
        "watching" : 2, # 3
        "on_hold" : 8, # 5
        "status" : "In class",
        "bio" : "Immersed in the magic of storytelling, I explore a myriad of genres from action-packed superhero epics to spine-tingling horror flicks, imaginative sci-fi odysseys, and heartwarming animated features. Constantly hunting for my next cinematic adventure, I revel in dissecting narratives and uncovering hidden gems. Let's bond over our mutual love for movies and TV shows, sharing our favorites and debating the latest plot twists!",
        "joined" : "January 8th, 2022",
        "birthdate" : "March 25",
        "gender" : "Male",
        "movies" : {
            "Inception": (1182444, "Completed"),
            "Fight Club" : (1406847, "Completed"),
            "The Matrix" : (1132806, "Completed"),
            "The Social Network": (1419997, "Completed"),
            "The Dark Knight" : (1386160, "Completed")
        },
        "series" : {
            "Blade Runner 2049": (153801, "Watching"),
            "War for the Planet of the Apes" : (1357314, "Watching"),
            "Logan" : (1461946, "On Hold")
        },
        "recent" : [
            1182444,
            1406847,
            1132806
        ],
        "friends" : [
            1,
            3,
            4
        ],
        "reviews" : [
            1386160,
            1419997
        ]
    },
    "dankskillz": {
        "id" : 3,
        "username" : "dankskillz",
        "profile_picture" : "https://cdn.myanimelist.net/s/common/userimages/3484be0c-3ae4-4411-ac04-2c686f92a51b_225w?s=531ad7cf9332297283e4ff09e23dad2d",
        "currently_watching": ["Inception", "The Matrix", "Oppenheimer"],
        "completed" : 1, # 1
        "watching" : 2, # 3
        "on_hold" : 8, # 5
        "status" : "At work",
        "bio" : "A connoisseur of diverse narratives, I journey through an array of genres including thrilling action, eerie horror, expansive sci-fi, and enchanting animated tales. Ever in search of the next gripping story, I cherish analyzing plot intricacies and character arcs. Let's connect over our passion for the screen, exchanging recommendations and diving deep into our favorite films and series!",
        "joined" : "April 10th, 2021",
        "birthdate" : "August 19",
        "gender" : "Male",
        "movies" : {
            "The Bourne Ultimatum": (1381053, "Completed"),
            "Avatar" : (138014, "Completed"),
            "The Martian" : (1406622, "Completed"),
            "The Dark Knight" : (1386160, "Completed")
        },
        "series" : {
            "Star Wars: The Force Awakens": (1359306, "Watching"),
            "Thor: Ragnarok" : (1431650, "On Hold"),
            "Stargate Universe" : (3102379, "On Hold")
        },
        "recent" : [
            1381053,
            138014,
            1406622
        ],
        "friends" : [
            2,
            1,
            4
        ],
        "reviews" : [
            1386160
        ]
    },
    "g4v1ng72": {
        "id" : 4,
        "username" : "g4v1ng72",
        "profile_picture" : "https://cdn.myanimelist.net/s/common/userimages/c21b7e17-a3d8-4e23-b70b-6f655903030e_225w?s=6e46e9233497e7c04f40d371dfd4e11a",
        "currently_watching": ["Inception", "The Matrix", "Oppenheimer"],
        "completed" : 1, # 1
        "watching" : 2, # 3
        "on_hold" : 8, # 5
        "status" : "Vibing",
        "bio" : "Captivated by the art of storytelling, I delve into genres ranging from adrenaline-fueled superhero sagas to bone-chilling horror, vast sci-fi realms, and delightful animated adventures. Always eager for my next viewing experience, I love discussing the layers and details of different narratives. Join me in celebrating our shared enthusiasm for movies and TV shows, and let's explore the cinematic world together!",
        "joined" : "May 17th, 2020",
        "birthdate" : "September 21",
        "gender" : "Male",
        "movies" : {
            "The Social Network": (1419997, "Completed"),
            "Saving Private Ryan" : (1334825, "Completed"),
            "Schindler's List" : (1335706, "Completed")
        },
        "series" : {
            "Titanic": (1434734, "On Hold"),
            "Casablanca" : (168295, "On Hold"),
            "Die Hard" : (1102562, "On Hold")
        },
        "recent" : [
            1419997,
            1334825,
            1335706
        ],
        "friends" : [
            2,
            3,
            1
        ]
    }
}

reviews = {
   1386160 : [("This may seem like faint praise, but about the highest compliment I can give Christopher Nolan's The Dark Knight right now is to say that there were many long stretches during which I didn't even realize it was a superhero movie. And, conversely (as SCTV's Joe Flaherty would say during a Charlton Heston impersonation) during those stretches in which I was reminded it was a superhero movie, I didn't wish it wasn't.", 90, users[2]['username'], users[2]['profile_picture'], len(users[2]['reviews']),"10/07/2008"), ("It doesn't matter how many superhero movies its crosstown rival makes; it'll never match the brilliance that Nolan delivered the same year Marvel began its infinite project. Firing on all cylinders … this is the most complete film Nolan has ever made.", 95, users[3]['username'], users[3]['profile_picture'], len(users[3]['reviews']), "05/19/2016")],
   1419997: [("With the likes of Zodiac (a sumptuous crime film with a long, mid-act ellipsis, and an inconclusive conclusion) and The Curious Case Of Benjamin Button (a flawed, inverted Forrest Gump substituting Baby Boomer nostalgia for textured Americana), Fincher has placed his full attentions on script, place and character, using his keen sense of production polish to lift his work out of its immediate cinematic context. He is one of the few directors working today who helms projects that gaze across broad horizons, from the classical past to the stylistic future. But The Social Network, while exhibiting the touch of a master filmmaker, is unmistakeably a film about the world we live in today.", 93, users[2]['username'], users[2]['profile_picture'], len(users[2]['reviews']), "10/15/2010")]
}

# VenomSlayer58 : Password56789

passwords = {
    "asder4215" : "Password12345",
    "Tym" : "Password23456",
    "dankskillz" : "Password34567",
    "g4v1ng72" : "Password45678",
}

def update_stats():
    """
    # Calculate counts for completed, on hold, and watching
    completed_count = sum(1 for movie in active_user["movies"].values() if movie[1] == "Completed") + \
                    sum(1 for series in active_user["series"].values() if series[1] == "Completed")

    on_hold_count = sum(1 for movie in active_user["movies"].values() if movie[1] == "On Hold") + \
                    sum(1 for series in active_user["series"].values() if series[1] == "On Hold")

    watching_count = sum(1 for movie in active_user["movies"].values() if movie[1] == "Watching") + \
                    sum(1 for series in active_user["series"].values() if series[1] == "Watching")

    # Update the user profile dictionary
    active_user["completed"] = completed_count
    active_user["on_hold"] = on_hold_count
    active_user["watching"] = watching_count
    """

    for inside_user in users:
        # Calculate counts for completed, on hold, and watching
        completed_count = sum(1 for movie in users[inside_user]["movies"].values() if movie[1] == "Completed") + \
                        sum(1 for series in users[inside_user]["series"].values() if series[1] == "Completed")

        on_hold_count = sum(1 for movie in users[inside_user]["movies"].values() if movie[1] == "On Hold") + \
                        sum(1 for series in users[inside_user]["series"].values() if series[1] == "On Hold")

        watching_count = sum(1 for movie in users[inside_user]["movies"].values() if movie[1] == "Watching") + \
                        sum(1 for series in users[inside_user]["series"].values() if series[1] == "Watching")

        # Update the user profile dictionary
        users[inside_user]["completed"] = completed_count
        users[inside_user]["on_hold"] = on_hold_count
        users[inside_user]["watching"] = watching_count

    for inside_user_again in users_names:
        # Calculate counts for completed, on hold, and watching
        completed_count = sum(1 for movie in users_names[inside_user_again]["movies"].values() if movie[1] == "Completed") + \
                        sum(1 for series in users_names[inside_user_again]["series"].values() if series[1] == "Completed")

        on_hold_count = sum(1 for movie in users_names[inside_user_again]["movies"].values() if movie[1] == "On Hold") + \
                        sum(1 for series in users_names[inside_user_again]["series"].values() if series[1] == "On Hold")

        watching_count = sum(1 for movie in users_names[inside_user_again]["movies"].values() if movie[1] == "Watching") + \
                        sum(1 for series in users_names[inside_user_again]["series"].values() if series[1] == "Watching")

        # Update the user profile dictionary
        users_names[inside_user_again]["completed"] = completed_count
        users_names[inside_user_again]["on_hold"] = on_hold_count
        users_names[inside_user_again]["watching"] = watching_count

update_stats()

def fetch_data(api_key, search_query):
    url = f"{base_url}{search_query}/details/?apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        ##print(f"Error fetching data: {response.status_code}")
        return None

def convert_data(data):
    processed_dictionary = dict()
    processed_dictionary['id'] = data['id']
    processed_dictionary['title'] = data['title']
    processed_dictionary['runtime'] = data['runtime_minutes']
    processed_dictionary['description'] = data['plot_overview']
    processed_dictionary['genre'] = data['genre_names']
    processed_dictionary['year'] = data['year']
    processed_dictionary['poster'] = data['poster']
    return processed_dictionary

def convert_friend(data):
    processed_dictionary = dict()
    processed_dictionary['id'] = data['id']
    processed_dictionary['username'] = data['username']
    processed_dictionary['status'] = data['status']
    processed_dictionary['joined'] = data['joined']
    processed_dictionary['birthdate'] = data['birthdate']
    processed_dictionary['profile_picture'] = data['profile_picture']
    processed_dictionary['bio'] = data['bio']
    return processed_dictionary

def chatGPT_summary(my_api_key, message):
    # Create an OpenAPI client using the key from our environment variable
    client = OpenAI(
        api_key=my_api_key,
    )

    # Specify the model to use and the messages to send
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a movie critic giving an unbiased overview of a specific movie to get someone else to watch it"},
            {"role": "user", "content": message}
        ]
    )
    return completion.choices[0].message.content

def generate(user_input):
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the CSV file
    csv_file_path = os.path.join(script_dir, 'title_id_map.csv')

    # Read the CSV file
    df = pd.read_csv(csv_file_path, dtype={'Year': 'string'})
    title = user_input
    results = df[df['Title'] == title]
    id = int(results['Watchmode ID'].iloc[0])

    # Fetch data from Watchmode API
    data = fetch_data(api_key, id)

    #print(data)

    data_new = convert_data(data)
    ##print(data_new)


    similar_movies = []
    for title_id in data['similar_titles']:
        title_result = df[df['Watchmode ID'] == title_id]
        movie = title_result['Title'].iloc[0]
        similar_movies.append(movie)


    if len(similar_movies) > 2:
        random_indices = random.sample(range(0, len(similar_movies) - 1), 3)
        list_here = []
        for index in random_indices:
            list_here.append(similar_movies[index])
        return list_here
    elif not similar_movies:
        lesser_list = []
        for movie in similar_movies:
            lesser_list.append(movie)
        return lesser_list
    else:
        return []

def summaries(similar_movies):
    if len(similar_movies) > 2:
        random_indices = random.sample(range(0, len(similar_movies) - 1), 3)
        list_here = []
        for index in random_indices:
            list_here.append(chatGPT_summary(gpt_api, f"Explain this movie: {similar_movies[index]}"))
        return list_here
    elif not similar_movies:
        lesser_list = []
        for movie in similar_movies:
            lesser_list.append(chatGPT_summary(gpt_api, f"Explain this movie: {movie}"))
        return lesser_list
    else:
        return []

def convert_to_embedded_link(link):
    video_id = link.split('v=')[1]
    embedded_link = f'https://www.youtube.com/embed/{video_id}'
    return embedded_link

app = Flask(__name__)

@app.route('/<string:user>/profile', methods=['GET'])
def displayUser(user):
    update_stats()
    this_user = users_names[user]
    make_bar(this_user['watching'], this_user['completed'], this_user['on_hold'])
    recent_dict = this_user['recent']
    recent = []
    #print("HELLO")
    #print(recent_dict)
    for entry in recent_dict:
        movie = fetch_data(api_key, entry)
        #print(movie)
        recent.append(movie)
    return render_template('user.html', user=this_user, recent=recent, movies=this_user['movies']) # home page

@app.route('/<string:user>/friends', methods=['GET'])
def friendsDisplay(user):
    this_user = users_names[user]
    users_list = []
    users_dictionary = this_user['friends']
    for inner_user in users_dictionary:
        ##print(users[inner_user])
        users_list.append(convert_friend(users[inner_user]))
    ##print(users_list)
    return render_template('friends.html', given_user=user, friends=users_list)

@app.route('/<string:user>/reviews', methods=['GET'])
def userReviews(user):
    given_user = users_names[user]
    reviews_of_user = given_user['reviews']

    reviews_list = []

    for item in reviews_of_user:
        for inner_review in reviews[item]:
            if inner_review[2] == user:
                
                connection, cursor = create_sqlite_db(csv_file, db_file)
                query = f'SELECT * FROM movies WHERE watchmode_id="{item}"'
                data = query_database(query, cursor)
                data = data[0]
                data = data[0]
                close_database_connection(connection)
                movie = fetch_data(api_key, data)
                title_of_movie = movie['title']
                poster_of_movie = movie['backdrop']

                copy = list(inner_review)
                copy.append(title_of_movie)
                copy.append(poster_of_movie)
                copy = tuple(copy)

                reviews_list.append(copy)

    print(reviews_list)
    print(reviews_of_user)

    return render_template('userreviews.html', reviews_of_user=reviews_list, current_user=given_user['username'], user_info=given_user)


# /The%20Dark%20Knight/review
# /The%20Social%20Network/review
@app.route('/<string:title>/review', methods=['GET'])
def movieReview(title):
    connection, cursor = create_sqlite_db(csv_file, db_file)
    query = f'SELECT * FROM movies WHERE title="{title}"'
    data = query_database(query, cursor)
    data = data[0]
    data = data[0]
    close_database_connection(connection)
    movie = fetch_data(api_key, data)
    #retrieved_review = reviews[movie['id']][0]
    #retrieved_score = reviews[movie['id']][1]
    #retrieved_user = users[reviews[movie['id']][2]]

    review_list = reviews[movie['id']]

    #print(data) #JSON
    return render_template('moviereview.html', title=movie["title"], review_list = review_list)

# @app.route('/<string:user>/reviews', methods=['GET'])

@app.route('/<string:user>/movies', methods=['GET'])
def display1(user):
    this_user = users_names[user]
    movies_dict = this_user['movies']
    movie_titles = []

    for title in movies_dict:
        connection, cursor = create_sqlite_db(csv_file, db_file)
        query = f'SELECT * FROM movies WHERE title="{title}"'
        data = query_database(query, cursor)
        data = data[0]
        #print(data)
        close_database_connection(connection)
        movie_entry = fetch_data(api_key, data[0])
        #print(movie_entry)
        standard_link = movie_entry['trailer']
        embedded_link = convert_to_embedded_link(standard_link)
        movie_titles.append([movie_entry, movies_dict[title][1], embedded_link])
    return render_template('movies.html', given_user=user, movie_titles=movie_titles)

# /currentlyairing

@app.route('/currentlyairing', methods=['GET'])
def displayingairing():
    movies = get_now_playing_movies(api_key_extra)
    return render_template('playing.html', movies_list=movies)

@app.route('/<string:user>/series', methods=['GET'])
def display2(user):
    this_user = users_names[user]
    series_dict = this_user['series']
    series_titles = []

    for title in series_dict:
        connection, cursor = create_sqlite_db(csv_file, db_file)
        query = f'SELECT * FROM movies WHERE title="{title}"'
        data = query_database(query, cursor)
        data = data[0]
        #print(data)
        close_database_connection(connection)
        series_entry = fetch_data(api_key, data[0])
        #print(series_entry)
        standard_link = series_entry['trailer']
        embedded_link = convert_to_embedded_link(standard_link)
        series_titles.append([series_entry, series_dict[title][1], embedded_link])
    return render_template('series.html', given_user=user, series_titles=series_titles)

@app.route('/<string:user>/all', methods=['GET'])
def display3(user):
    this_user = users_names[user]
    movies_dict = this_user['movies']
    movie_titles = []

    for title in movies_dict:
        connection, cursor = create_sqlite_db(csv_file, db_file)
        query = f'SELECT * FROM movies WHERE title="{title}"'
        data = query_database(query, cursor)
        data = data[0]
        #print(data)
        close_database_connection(connection)
        movie_entry = fetch_data(api_key, data[0])
        #print(movie_entry)
        standard_link = movie_entry['trailer']
        embedded_link = convert_to_embedded_link(standard_link)
        movie_titles.append([movie_entry, movies_dict[title][1], embedded_link])
    
    series_dict = this_user['series']
    series_titles = []

    for title in series_dict:
        connection, cursor = create_sqlite_db(csv_file, db_file)
        query = f'SELECT * FROM movies WHERE title="{title}"'
        data = query_database(query, cursor)
        data = data[0]
        #print(data)
        close_database_connection(connection)
        series_entry = fetch_data(api_key, data[0])
        #print(series_entry)
        standard_link = series_entry['trailer']
        embedded_link = convert_to_embedded_link(standard_link)
        series_titles.append([series_entry, series_dict[title][1], embedded_link])
    return render_template('all.html', given_user=user, movie_titles=movie_titles, series_titles=series_titles)


@app.route('/reelrecs')
def recs():
    return render_template('input.html') # home page

@app.route('/searchuser')
def finduser():
    return render_template('searchuser.html') # home page

@app.route('/searchmovie')
def findmovie():
    return render_template('findmovie.html') # home page

@app.route('/additem')
def additem():
    return render_template('addmovie.html') # home page

@app.route('/addreview')
def addreview():
    return render_template('addreview.html') # home page

@app.route('/addingfriend')
def addingfriendscreen():
    return render_template('addfriend.html')

@app.route('/addfriend/<string:user_planned>')
def addingfriend(user_planned):
    global active_user
    active_user_here = active_user['id']
    active_user_here_name = active_user['username']
    current_id_here = users_names[user_planned]['id']
    users[active_user_here]['friends'].append(current_id_here)
    users_names[active_user_here_name]['friends'].append(current_id_here)

    return redirect(url_for('active'))


@app.route('/editprofile')
def editing():
    return render_template('editprofile.html')

# /create/VenomSlayer58

@app.route('/create/<string:user_planned>/<string:password>')
def create(user_planned, password, methods=['GET']):
    user_to_make = user_planned
    passwords[user_planned] = password
    return render_template('createprofile.html', user_ready=user_to_make)

@app.route('/loggingin/<string:user_access>/<string:password>')
def getinside(user_access, password):
    global active_user
    active_user = users[users_names[user_access]['id']]

    if password == passwords[user_access]:
        print("Login Successful")

    return redirect(url_for('active'))

# Directory to save uploaded profile pictures
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/createprofile/<string:user_made>', methods=['POST'])
def creating(user_made):
    gender = request.form['gender']
    birthdate = request.form['birthdate']
    status = request.form['status']
    bio = request.form['bio']
    profile_pic = request.files['profile_pic']
    joining = convert_current_date(get_current_date())
    
    # Print the form data
    print(gender)
    birthdate = convert_date(birthdate)
    print(birthdate)
    print(status)
    print(bio)
    print(joining)
    
    # Check if the profile picture was uploaded
    if profile_pic:
        # Create the uploads folder if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        unique_filename = f"{user_made}{os.path.splitext(profile_pic.filename)[1]}"
        # Save the uploaded file to the uploads folder
        profile_pic_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        profile_pic.save(profile_pic_path)
        print(f"Profile picture saved to {profile_pic_path}")

    print(convert_backslashes_to_slashes(profile_pic_path))

    print(len(users))
    print(users)

    print(len(users_names))
    print(user_made)

    users[len(users) + 1] = dict()
    users_names[user_made] = dict()

    #####
    users[len(users)]['id'] = len(users)
    users_names[user_made]['id'] = len(users)

    users[len(users)]['gender'] = gender
    users_names[user_made]['gender'] = gender

    users[len(users)]['status'] = status
    users_names[user_made]['status'] = status

    users[len(users)]['birthdate'] = birthdate
    users_names[user_made]['birthdate'] = birthdate

    users[len(users)]['bio'] = bio
    users_names[user_made]['bio'] = bio

    users[len(users)]['joined'] = joining
    users_names[user_made]['joined'] = joining

    users[len(users)]['username'] = user_made
    users_names[user_made]['username'] = user_made

    users[len(users)]['currently_watching'] = []
    users_names[user_made]['currently_watching'] = []

    users[len(users)]['completed'] = 0
    users_names[user_made]['completed'] = 0

    users[len(users)]['watching'] = 0
    users_names[user_made]['watching'] = 0

    users[len(users)]['on_hold'] = 0
    users_names[user_made]['on_hold'] = 0

    users[len(users)]['movies'] = dict()
    users_names[user_made]['movies'] = dict()

    users[len(users)]['series'] = dict()
    users_names[user_made]['series'] = dict()

    users[len(users)]['recent'] = []
    users_names[user_made]['recent'] = []

    users[len(users)]['friends'] = []
    users_names[user_made]['friends'] = []

    users[len(users)]['reviews'] = []
    users_names[user_made]['reviews'] = []

    #users[len(users)]['profile_pic'] = "/" + convert_backslashes_to_slashes(profile_pic_path)
    #users_names[user_made]['profile_pic'] = "/" + convert_backslashes_to_slashes(profile_pic_path)


    # /static/images/testUser5.jpg

    users[len(users)]['profile_picture'] = "/" + convert_backslashes_to_slashes(profile_pic_path)
    users_names[user_made]['profile_picture'] = "/" + convert_backslashes_to_slashes(profile_pic_path)

    print("/" + convert_backslashes_to_slashes(profile_pic_path))

    #login
    return redirect(url_for('login'))

@app.route('/editprofile/<string:gender>/<string:status>/<string:bio>', methods=['GET'])
def processingprofile(gender, status, bio):

    if gender != "empty":
        active_user["gender"] = gender
        users[active_user["id"]]['gender'] = gender
        users_names[users[active_user["id"]]['username']]['gender'] = gender

    if status != "empty":
        active_user["status"] = status
        users[active_user["id"]]['status'] = status
        users_names[users[active_user["id"]]['username']]['status'] = status

    if bio != "empty":
        active_user["bio"] = bio
        users[active_user["id"]]['bio'] = bio
        users_names[users[active_user["id"]]['username']]['bio'] = bio

    return redirect(url_for('active'))


@app.route('/reviewsearch')
def searchreview():
    return render_template('findreview.html') # home page

@app.route('/')
def welcoming():
    global active_user
    active_user = dict()
    return render_template('welcome.html')

@app.route('/get-started')
def gettingstarted():
    return render_template('gettingstarted.html')

@app.route('/createaccount')
def createaccountscreen():
    return render_template('creationscreen.html')

@app.route('/login')
def login():
    return render_template('login.html')

# will become the /reelrecs route
@app.route('/dashboard')
def active():
    global active_user

    update_stats()
    user = active_user
    print(user)
    make_bar(user['watching'], user['completed'], user['on_hold'])
    recent_dict = user['recent']
    recent = []
    #print("HELLO")
    #print(recent_dict)
    for entry in recent_dict:
        movie = fetch_data(api_key, entry)
        #print(movie)
        recent.append(movie)
    return render_template('home.html', user=user, recent=recent, movies=user['movies']) # home page

@app.route('/processed/<string:type>/<string:process>/<string:title>', methods=['GET'])
def processing(type, process, title):
    connection, cursor = create_sqlite_db(csv_file, db_file)
    query = f'SELECT * FROM movies WHERE title="{title}"'
    data = query_database(query, cursor)
    data = data[0]
    data = data[0]
    close_database_connection(connection)
    
    print(active_user)

    true_user = active_user['id']
    true_user = users[true_user]
    true_user_plus = users_names[true_user["username"]]

    kind = ""

    if process == "Completed":
        kind = "Completed"
    elif process == "Watching":
        kind = "Watching"
    elif process == "OnHold":
        kind = "On Hold"

    if type == "Movie":
        true_user["movies"][title] = (data, kind)
        true_user_plus["movies"][title] = (data, kind)
    elif type == "Series":
        true_user["series"][title] = (data, kind)
        true_user_plus["series"][title] = (data, kind)
    
    if process == "Completed":
        if len(true_user["recent"]) == 3:
            true_user["recent"].pop()
            true_user_plus["recent"].pop()
        true_user["recent"].insert(0, data)    
        true_user_plus["recent"].insert(0, data)

    recent_dict = active_user['recent']

    recent = []
    #print("HELLO")
    #print(recent_dict)
    for entry in recent_dict:
        movie = fetch_data(api_key, entry)
        #print(movie)
        recent.append(movie)

    update_stats()
    make_bar(active_user['watching'], active_user['completed'], active_user['on_hold'])

    return redirect(url_for('active'))

@app.route('/processedreview/<string:type>/<string:title>/<string:review>/<string:rating>', methods=['GET'])
def processreview(type, title, review, rating):
    connection, cursor = create_sqlite_db(csv_file, db_file)
    query = f'SELECT * FROM movies WHERE title="{title}"'
    data = query_database(query, cursor)
    data = data[0]
    data = data[0]
    close_database_connection(connection)
    movie = fetch_data(api_key, data)
    movie_id = movie['id']

    current_date = get_current_date()

    if movie_id not in reviews:
        reviews[movie_id] = [(review, int(rating), users[active_user["id"]]['username'], users[active_user["id"]]['profile_picture'], len(users[active_user["id"]]['reviews']) + 1, current_date)]
    else:
        reviews[movie_id].append((review, int(rating), users[active_user["id"]]['username'], users[active_user["id"]]['profile_picture'], len(users[active_user["id"]]['reviews']) + 1, current_date))
    
    if movie_id not in active_user["reviews"]:
        active_user["reviews"].append(movie_id)
    if movie_id not in users[active_user["id"]]['reviews']:
        users[active_user["id"]]['reviews'].append(movie_id)
    if movie_id not in users_names[users[active_user["id"]]['username']]['reviews']:
        users_names[users[active_user["id"]]['username']]['reviews'].append(movie_id)

    print(active_user["reviews"])
    print(users[active_user["id"]]['reviews'])
    print(users_names[users[active_user["id"]]['username']]['reviews'])

    return redirect(url_for('active'))

@app.route('/movie/<string:title>', methods=['GET']) # GET request because just requesting info from server
def learn(title):
    item = None
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the CSV file
    csv_file_path = os.path.join(script_dir, 'title_id_map.csv')

    # Read the CSV file
    df = pd.read_csv(csv_file_path, dtype={'Year': 'string'})
    
    suggested_titles = generate(title)
    titles_data = []
    for movie in suggested_titles:
        title_result = df[df['Title'] == movie]
        id = int(title_result['Watchmode ID'].iloc[0])
        titles_data.append(id)

    complete_data = []
    for inner_id in titles_data:
        complete_data.append(fetch_data(api_key, inner_id))
    #print(complete_data)

    return render_template('movie.html', item=item, title=title, items=complete_data)

@app.route('/overview/<string:title>', methods=['GET']) # GET request because just requesting info from server
def learn2(title):
    item = None
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the CSV file
    csv_file_path = os.path.join(script_dir, 'title_id_map.csv')

    # Read the CSV file
    df = pd.read_csv(csv_file_path, dtype={'Year': 'string'})
    better_summary = chatGPT_summary(gpt_api, f"Explain this movie: {title}")

    title_result = df[df['Title'] == title]
    id = int(title_result['Watchmode ID'].iloc[0])
    data = fetch_data(api_key, id)
    #print(data)
    standard_link = data['trailer']
    embedded_link = convert_to_embedded_link(standard_link)

    return render_template('main.html', item=item, title=title, movie=data, trailer=embedded_link, sum=better_summary)


@app.route('/readme', methods=['GET']) # GET request because just requesting info from server
def learn3():
    return render_template('readme.html')

if __name__ == '__main__':
   app.run(debug = True)