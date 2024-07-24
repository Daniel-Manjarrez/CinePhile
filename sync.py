import os
import json
import portalocker

"""
passwords = {
    "asder4215" : "Password12345",
    "Tym" : "Password23456",
    "dankskillz" : "Password34567",
    "g4v1ng72" : "Password45678",
    "VenomSlayer" : "SeoTech123",
    "Danbeza45" : "SeoTech456", 
    "Abdumu78" : "SeoTech789"
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
        ],
        "reviews" : [
            
        ]
    },
    5: {
        "id" : 5,
        "username" : "VenomSlayer",
        "profile_picture" : "https://cdn.myanimelist.net/s/common/userimages/04773549-2aa9-48f2-83a0-e00eee70ef58_225w?s=ae03e775664fe00fe831dec8a741348a",
        "currently_watching": [],
        "completed" : 0, # 1
        "watching" : 0, # 3
        "on_hold" : 0, # 5
        "status" : "Relaxing",
        "bio" : "Passionate about superhero movies, I love diving deep into captivating storylines and thrilling adventures. Whether it's epic battles, origin stories, or ensemble blockbusters, I enjoy delving into the intricacies of each narrative. Always on the lookout for my next great watch, let's geek out over our favorite superhero flicks together!",
        "joined" : "July 23rd, 2024",
        "birthdate" : "February 17",
        "gender" : "Male",
        "movies" : {},
        "series" : {},
        "recent" : [],
        "friends" : [],
        "reviews" : []
    },
    6: {
        "id" : 6,
        "username" : "Danbeza45",
        "profile_picture" : "https://cdn.myanimelist.net/s/common/userimages/c083cad7-41a3-46b5-931e-e1d62c6b9fd2_225w?s=be5edf7c281dc1fa5ff171d24aade21b",
        "currently_watching": [],
        "completed" : 0, # 1
        "watching" : 0, # 3
        "on_hold" : 0, # 5
        "status" : "Resting",
        "bio" : "Passionate about horror movies, I love diving deep into spine-chilling storylines and eerie atmospheres. Whether it's psychological thrillers, supernatural tales, or slasher flicks, I enjoy exploring the intricacies of each narrative. Always on the lookout for my next great scare, let's geek out over our favorite horror films together!",
        "joined" : "July 21st, 2024",
        "birthdate" : "April 11",
        "gender" : "Male",
        "movies" : {},
        "series" : {},
        "recent" : [],
        "friends" : [],
        "reviews" : []
    },
    7: {
        "id" : 7,
        "username" : "Abdumu78",
        "profile_picture" : "https://cdn.myanimelist.net/s/common/userimages/8f3e8237-3acb-4db2-af15-8b0ff22ef842_225w?s=3b4abe79a94a6daf1077957bc0a4eea9",
        "currently_watching": [],
        "completed" : 0, # 1
        "watching" : 0, # 3
        "on_hold" : 0, # 5
        "status" : "Living",
        "bio" : "Passionate about action and thriller movies, I love diving deep into captivating storylines and pulse-pounding adventures. Whether it's high-stakes heists, intense combat scenes, or edge-of-your-seat suspense, I enjoy exploring the intricacies of each narrative. Always on the lookout for my next great watch, let's geek out over our favorite action and thriller flicks together!",
        "joined" : "July 22nd, 2024",
        "birthdate" : "March 29",
        "gender" : "Male",
        "movies" : {},
        "series" : {},
        "recent" : [],
        "friends" : [],
        "reviews" : []
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
        ],
        "reviews" : []
    },
    "VenomSlayer" : {
        "id" : 5,
        "username" : "VenomSlayer",
        "profile_picture" : "https://cdn.myanimelist.net/s/common/userimages/04773549-2aa9-48f2-83a0-e00eee70ef58_225w?s=ae03e775664fe00fe831dec8a741348a",
        "currently_watching": [],
        "completed" : 0, # 1
        "watching" : 0, # 3
        "on_hold" : 0, # 5
        "status" : "Relaxing",
        "bio" : "Passionate about superhero movies, I love diving deep into captivating storylines and thrilling adventures. Whether it's epic battles, origin stories, or ensemble blockbusters, I enjoy delving into the intricacies of each narrative. Always on the lookout for my next great watch, let's geek out over our favorite superhero flicks together!",
        "joined" : "July 23rd, 2024",
        "birthdate" : "February 17",
        "gender" : "Male",
        "movies" : {},
        "series" : {},
        "recent" : [],
        "friends" : [],
        "reviews" : []
    },
    "Danbeza45" : {
        "id" : 6,
        "username" : "Danbeza45",
        "profile_picture" : "https://cdn.myanimelist.net/s/common/userimages/c083cad7-41a3-46b5-931e-e1d62c6b9fd2_225w?s=be5edf7c281dc1fa5ff171d24aade21b",
        "currently_watching": [],
        "completed" : 0, # 1
        "watching" : 0, # 3
        "on_hold" : 0, # 5
        "status" : "Resting",
        "bio" : "Passionate about horror movies, I love diving deep into spine-chilling storylines and eerie atmospheres. Whether it's psychological thrillers, supernatural tales, or slasher flicks, I enjoy exploring the intricacies of each narrative. Always on the lookout for my next great scare, let's geek out over our favorite horror films together!",
        "joined" : "July 21st, 2024",
        "birthdate" : "April 11",
        "gender" : "Male",
        "movies" : {},
        "series" : {},
        "recent" : [],
        "friends" : [],
        "reviews" : []
    }, 
    "Abdumu78" : {
        "id" : 7,
        "username" : "Abdumu78",
        "profile_picture" : "https://cdn.myanimelist.net/s/common/userimages/8f3e8237-3acb-4db2-af15-8b0ff22ef842_225w?s=3b4abe79a94a6daf1077957bc0a4eea9",
        "currently_watching": [],
        "completed" : 0, # 1
        "watching" : 0, # 3
        "on_hold" : 0, # 5
        "status" : "Living",
        "bio" : "Passionate about action and thriller movies, I love diving deep into captivating storylines and pulse-pounding adventures. Whether it's high-stakes heists, intense combat scenes, or edge-of-your-seat suspense, I enjoy exploring the intricacies of each narrative. Always on the lookout for my next great watch, let's geek out over our favorite action and thriller flicks together!",
        "joined" : "July 22nd, 2024",
        "birthdate" : "March 29",
        "gender" : "Male",
        "movies" : {},
        "series" : {},
        "recent" : [],
        "friends" : [],
        "reviews" : []
    }
}
reviews = {
   1386160 : [("This may seem like faint praise, but about the highest compliment I can give Christopher Nolan's The Dark Knight right now is to say that there were many long stretches during which I didn't even realize it was a superhero movie. And, conversely (as SCTV's Joe Flaherty would say during a Charlton Heston impersonation) during those stretches in which I was reminded it was a superhero movie, I didn't wish it wasn't.", 90, users[2]['username'], users[2]['profile_picture'], len(users[2]['reviews']),"10/07/2008"), ("It doesn't matter how many superhero movies its crosstown rival makes; it'll never match the brilliance that Nolan delivered the same year Marvel began its infinite project. Firing on all cylinders … this is the most complete film Nolan has ever made.", 95, users[3]['username'], users[3]['profile_picture'], len(users[3]['reviews']), "05/19/2016")],
   1419997: [("With the likes of Zodiac (a sumptuous crime film with a long, mid-act ellipsis, and an inconclusive conclusion) and The Curious Case Of Benjamin Button (a flawed, inverted Forrest Gump substituting Baby Boomer nostalgia for textured Americana), Fincher has placed his full attentions on script, place and character, using his keen sense of production polish to lift his work out of its immediate cinematic context. He is one of the few directors working today who helms projects that gaze across broad horizons, from the classical past to the stylistic future. But The Social Network, while exhibiting the touch of a master filmmaker, is unmistakeably a film about the world we live in today.", 93, users[2]['username'], users[2]['profile_picture'], len(users[2]['reviews']), "10/15/2010")]
}
"""

### PASSWORDS INTERFACE ###

def write_passwords_to_file(passwords, filename='passwords.txt'):
    with open(filename, 'w') as file:
        portalocker.lock(file, portalocker.LOCK_EX)
        for username, password in passwords.items():
            file.write(f"{username}:{password}\n")
        portalocker.unlock(file)

# write_passwords_to_file(passwords)

def read_passwords_from_file(filename='passwords.txt'):
    passwords = {}
    with open(filename, 'r') as file:
        portalocker.lock(file, portalocker.LOCK_SH)
        for line in file:
            username, password = line.strip().split(':')
            passwords[username] = password
        portalocker.unlock(file)
    return passwords

def add_password(username, password, filename='passwords.txt'):
    # Read existing passwords
    passwords = read_passwords_from_file(filename)
    
    # Add new password
    passwords[username] = password
    
    # Write updated passwords back to file
    write_passwords_to_file(passwords, filename)

"""
passwords = read_passwords_from_file()
print(passwords)
print()
add_password('new_user', 'new_password123')
print(read_passwords_from_file())  # Verify the new password was added
"""

### USERS INTERFACE ###

def write_users_to_file(users, filename='users.txt'):
    with open(filename, 'w') as file:
        portalocker.lock(file, portalocker.LOCK_EX)
        for user_id, user_data in users.items():
            file.write(f"{user_id}:{json.dumps(user_data)}\n")
        portalocker.unlock(file)

# write_users_to_file(users)

def read_users_from_file(filename='users.txt'):
    users = {}
    with open(filename, 'r') as file:
        portalocker.lock(file, portalocker.LOCK_SH)
        for line in file:
            user_id, user_data = line.strip().split(':', 1)
            users[int(user_id)] = json.loads(user_data)
        portalocker.unlock(file)
    return users

# users = read_users_from_file()
# print(users)  # Verify the dictionary is read correctly

def add_user(user_data, filename='users.txt'):
    # Read existing users
    users = read_users_from_file(filename)
    
    # Determine new user ID
    new_id = max(users.keys(), default=0) + 1
    user_data['id'] = new_id
    
    # Add new user
    users[new_id] = user_data
    
    # Write updated users back to file
    write_users_to_file(users, filename)

# Example usage
"""
new_user = {
    "username" : "new_user",
    "profile_picture" : "https://example.com/new_user.png",
    "currently_watching": ["Movie 1", "Movie 2"],
    "completed" : 0,
    "watching" : 2,
    "on_hold" : 0,
    "status" : "Active",
    "bio" : "New user bio",
    "joined" : "July 24th, 2024",
    "birthdate" : "January 1",
    "gender" : "Other",
    "movies" : {},
    "series" : {},
    "recent" : [],
    "friends" : [],
    "reviews" : []
}
"""

"""
add_user(new_user)
print(read_users_from_file())  # Verify the new user was added
"""

### USERS_NAMES INTERFACE ###

def write_users_names_to_file(users_names, filename='users_names.txt'):
    with open(filename, 'w') as file:
        portalocker.lock(file, portalocker.LOCK_EX)
        for username, user_data in users_names.items():
            file.write(f"{username}:{json.dumps(user_data)}\n")
        portalocker.unlock(file)

# write_users_names_to_file(users_names)

def read_users_names_from_file(filename='users_names.txt'):
    users_names = {}
    with open(filename, 'r') as file:
        portalocker.lock(file, portalocker.LOCK_SH)
        for line in file:
            username, user_data = line.strip().split(':', 1)
            users_names[username] = json.loads(user_data)
        portalocker.unlock(file)
    return users_names

# users_names = read_users_names_from_file()
# print(users_names)  # Verify the dictionary is read correctly

def add_user_name(user_data, filename='users_names.txt'):
    # Read existing users
    users_names = read_users_names_from_file(filename)
    
    # Determine new user ID
    new_id = max([user['id'] for user in users_names.values()], default=0) + 1
    user_data['id'] = new_id
    
    # Add new user
    users_names[user_data['username']] = user_data
    
    # Write updated users back to file
    write_users_names_to_file(users_names, filename)

# Example usage
"""
new_user = {
    "username": "new_user",
    "profile_picture": "https://example.com/new_user.png",
    "currently_watching": ["Movie 1", "Movie 2"],
    "completed": 0,
    "watching": 2,
    "on_hold": 0,
    "status": "Active",
    "bio": "New user bio",
    "joined": "July 24th, 2024",
    "birthdate": "January 1",
    "gender": "Other",
    "movies": {},
    "series": {},
    "recent": [],
    "friends": [],
    "reviews": []
}
"""

"""
add_user_name(new_user)
print(read_users_names_from_file())  # Verify the new user was added
"""

### REVIEWS INTERFACE ###

def write_reviews_to_file(reviews, filename='reviews.txt'):
    with open(filename, 'w') as file:
        portalocker.lock(file, portalocker.LOCK_EX)
        for movie_id, review_list in reviews.items():
            file.write(f"{movie_id}:{json.dumps(review_list)}\n")
        portalocker.unlock(file)

# write_reviews_to_file(reviews)

def read_reviews_from_file(filename='reviews.txt'):
    reviews = {}
    with open(filename, 'r') as file:
        portalocker.lock(file, portalocker.LOCK_SH)
        for line in file:
            movie_id, review_list = line.strip().split(':', 1)
            reviews[int(movie_id)] = json.loads(review_list)
        portalocker.unlock(file)
    return reviews

# reviews = read_reviews_from_file()
# print(reviews)  # Verify the dictionary is read correctly

def add_review(movie_id, review, filename='reviews.txt'):
    # Read existing reviews
    reviews = read_reviews_from_file(filename)
    
    # Add new review
    if movie_id in reviews:
        reviews[movie_id].append(review)
    else:
        reviews[movie_id] = [review]
    
    # Write updated reviews back to file
    write_reviews_to_file(reviews, filename)

# Example usage
"""
new_review = (
    "An incredible journey through time and space, a must-watch!",
    98,
    "new_user",
    "https://example.com/new_user.png",
    1,  # Number of reviews
    "07/24/2024"
)
"""

"""
add_review(1234567, new_review)
print(read_reviews_from_file())  # Verify the new review was added
"""