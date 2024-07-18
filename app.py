from flask import Flask
from flask import render_template, redirect, url_for
import os
import openai
import requests
import json
import random
import pandas as pd
from database_interface import print_all_entries
from database_interface import close_database_connection
from database_interface import query_database
from database_interface import print_query_retrieval
from database_interface import create_sqlite_db
from bar_interface import make_bar
from openai import OpenAI


#api_key = '8YQ53Ao5sqOGEq826OfsK3PqOEQBWY36Iv0KJsTx'
api_key = 'PWl8rjzz0vKsh3iYFRNfp7b3rzxMWO9hQgSxhQSD'
base_url = 'https://api.watchmode.com/v1/title/'
gpt_api = ""

csv_file = 'title_id_map.csv'
db_file = 'movies.db'

active_user = {
    "id" : 1,
    "profile" : {
        "username" : "asder4215",
        "profile_picture" : "https://cdn.myanimelist.net/s/common/userimages/dd32b9ac-4642-4743-936f-c551486b3396_225w?s=952a217493e230e0141e16d4c1fe5be7",
        "currently_watching": ["Inception", "The Matrix", "Oppenheimer"],
        "completed" : 5, # 1
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
            "Batman Begins" : (144341, "On Hold"),
            "Justice League" : (1196323, "Completed"),
            "Dark Phoenix" : (1472956, "Completed"),
        },
        "series" : {
            "Spider-Man: No Way Home": (1589918, "Watching"),
            "Spider-Man: Far From Home" : (1357314, "Completed"),
            "Spider-Man: Homecoming" : (1357316, "On Hold")
        },
        "recent" : [
            1196323,
            1472956,
            1386160
        ],
        "friends" : [
            2,
            3,
            4
        ]
    } 
}

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
            "The Matrix" : (1132806, "Completed")
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
            "The Martian" : (1406622, "Completed")
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
            "The Matrix" : (1132806, "Completed")
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
            "The Martian" : (1406622, "Completed")
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

def update_stats():
    # Calculate counts for completed, on hold, and watching
    completed_count = sum(1 for movie in active_user["profile"]["movies"].values() if movie[1] == "Completed") + \
                    sum(1 for series in active_user["profile"]["series"].values() if series[1] == "Completed")

    on_hold_count = sum(1 for movie in active_user["profile"]["movies"].values() if movie[1] == "On Hold") + \
                    sum(1 for series in active_user["profile"]["series"].values() if series[1] == "On Hold")

    watching_count = sum(1 for movie in active_user["profile"]["movies"].values() if movie[1] == "Watching") + \
                    sum(1 for series in active_user["profile"]["series"].values() if series[1] == "Watching")

    # Update the user profile dictionary
    active_user["profile"]["completed"] = completed_count
    active_user["profile"]["on_hold"] = on_hold_count
    active_user["profile"]["watching"] = watching_count

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

@app.route('/additem')
def additem():
    return render_template('addmovie.html') # home page

# will become the /reelrecs route
@app.route('/')
def start():
    update_stats()
    user = active_user
    make_bar(user['profile']['watching'], user['profile']['completed'], user['profile']['on_hold'])
    recent_dict = user['profile']['recent']
    recent = []
    #print("HELLO")
    #print(recent_dict)
    for entry in recent_dict:
        movie = fetch_data(api_key, entry)
        #print(movie)
        recent.append(movie)
    return render_template('home.html', user=user['profile'], recent=recent, movies=user['profile']['movies']) # home page

@app.route('/processed/<string:type>/<string:process>/<string:title>', methods=['GET'])
def processing(type, process, title):
    connection, cursor = create_sqlite_db(csv_file, db_file)
    query = f'SELECT * FROM movies WHERE title="{title}"'
    data = query_database(query, cursor)
    data = data[0]
    data = data[0]
    close_database_connection(connection)

    true_user = active_user["id"]
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
        active_user["profile"]["movies"][title] = (data, kind)
        true_user["movies"][title] = (data, kind)
        true_user_plus["movies"][title] = (data, kind)
    elif type == "Series":
        active_user["profile"]["series"][title] = (data, kind)
        true_user["series"][title] = (data, kind)
        true_user_plus["series"][title] = (data, kind)
    
    if process == "Completed":
        active_user['profile']['recent'].pop()
        active_user['profile']['recent'].insert(0, data)
        true_user["recent"].pop()
        true_user["recent"].insert(0, data)
        true_user_plus["recent"].pop()
        true_user_plus["recent"].insert(0, data)

    recent_dict = active_user['profile']['recent']

    recent = []
    #print("HELLO")
    #print(recent_dict)
    for entry in recent_dict:
        movie = fetch_data(api_key, entry)
        #print(movie)
        recent.append(movie)

    update_stats()
    make_bar(active_user['profile']['watching'], active_user['profile']['completed'], active_user['profile']['on_hold'])

    return redirect(url_for('start'))


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