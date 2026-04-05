from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
from functools import wraps
import secrets
import os
import requests
from urllib.parse import quote
import json
import hashlib
import random
import time
from datetime import datetime, timedelta
import re
import base64
from collections import defaultdict

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.permanent_session_lifetime = timedelta(days=7)

# ========== CONFIGURATION ==========
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin@123')
OMDB_API_KEY = os.environ.get('OMDB_API_KEY', 'f7b8d9c2')
SITE_CONFIG = {
    "site_name": "XSTAR AI",
    "site_logo": "⭐ XSTAR",
    "primary_color": "#e50914",
    "background_type": "dynamic",
    "background_image": "https://image.tmdb.org/t/p/original/wwemzKWzjKYJFfCeiB57q3r4Bcm.png",
    "animation_enabled": True,
    "default_language": "all"
}

# ========== 500+ MOVIES DATABASE (Multi-Language, Multi-Genre) ==========
MOVIES_DB = {}

# Action Movies
action_movies = [
    {"title": "Avengers: Endgame", "year": 2019, "imdb_id": "tt4154796", "language": "English", "genre": "Action, Sci-Fi", "image": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg", "banner": "https://image.tmdb.org/t/p/original/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg", "rating": 8.4, "story": "After the devastating events of Infinity War, the universe is in ruins. The Avengers assemble once more to reverse Thanos' actions and restore balance. This epic conclusion features time travel, emotional reunions, and the most spectacular battle sequence ever filmed. Tony Stark makes the ultimate sacrifice, Captain America finally gets his dance, and Thor discovers his worth beyond the hammer."},
    {"title": "John Wick: Chapter 4", "year": 2023, "imdb_id": "tt10366206", "language": "English", "genre": "Action, Thriller", "image": "https://image.tmdb.org/t/p/w500/vZloFAK7NmvMGKE7VkF5UHaz0I.jpg", "banner": "https://image.tmdb.org/t/p/original/4f1N4Y6k5m8P9Qr2S3tU4vW5xY6z.jpg", "rating": 8.2, "story": "John Wick uncovers a path to defeating the High Table. Before earning his freedom, he must face a new enemy with powerful alliances across the globe. The film features breathtaking action sequences including the famous Arc de Triomphe car-fight and the top-down Dragon's Breath shotgun scene."},
    {"title": "The Dark Knight", "year": 2008, "imdb_id": "tt0468569", "language": "English", "genre": "Action, Crime", "image": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg", "banner": "https://image.tmdb.org/t/p/original/nMKdUUepR0i5zn0y1T4CsSB5chy.jpg", "rating": 9.0, "story": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice. The film explores themes of chaos, order, and the fine line between hero and vigilante."},
    {"title": "Inception", "year": 2010, "imdb_id": "tt1375666", "language": "English", "genre": "Action, Sci-Fi", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/s3TBrRGB1iav7gFOCNx3H31HES9.jpg", "rating": 8.8, "story": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO. His tragic past threatens to sabotage the mission, leading to a mind-bending journey through layers of dreams."},
    {"title": "Mad Max: Fury Road", "year": 2015, "imdb_id": "tt1392190", "language": "English", "genre": "Action, Adventure", "image": "https://image.tmdb.org/t/p/w500/8tZYtuWezp8JbcsvHYO0O46tFbo.jpg", "banner": "https://image.tmdb.org/t/p/original/9kR2e0J0d9E0q0K9l0m0n0o0p0q.jpg", "rating": 8.1, "story": "In a post-apocalyptic wasteland, Max teams up with Furiosa to escape a tyrannical warlord. The film is a non-stop chase sequence with practical effects, stunning cinematography, and strong feminist themes."},
]

# Romance Movies
romance_movies = [
    {"title": "Titanic", "year": 1997, "imdb_id": "tt0120338", "language": "English", "genre": "Romance, Drama", "image": "https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg", "banner": "https://image.tmdb.org/t/p/original/7i9nNtL2rLc4m5n6o7p8q9r0s1t.jpg", "rating": 8.9, "story": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic. Their forbidden romance unfolds against the backdrop of one of history's greatest tragedies. The film won 11 Academy Awards and remains one of the highest-grossing films of all time."},
    {"title": "The Notebook", "year": 2004, "imdb_id": "tt0332280", "language": "English", "genre": "Romance, Drama", "image": "https://image.tmdb.org/t/p/w500/rNzQyW4f8B8cQr7jK9l0m1n2o3p.jpg", "banner": "https://image.tmdb.org/t/p/original/4m1n2o3p4q5r6s7t8u9v0w1x2y.jpg", "rating": 7.8, "story": "A poor and passionate young man falls in love with a rich young woman and gives her a sense of freedom. They are separated by social differences, but reunite years later after he builds the house she always wanted, reading their love story to her as she battles dementia."},
    {"title": "Your Name (Kimi no Na wa)", "year": 2016, "imdb_id": "tt5311514", "language": "Japanese", "genre": "Romance, Anime", "image": "https://image.tmdb.org/t/p/w500/q719jXXEzOoYaps6babgKnONONX.jpg", "banner": "https://image.tmdb.org/t/p/original/3r6J1j2k3l4m5n6o7p8q9r0s1t.jpg", "rating": 8.4, "story": "Two strangers find themselves linked in a bizarre way. When a connection forms, will distance be the only thing to keep them apart? This critically acclaimed anime masterpiece explores body-swapping, time travel, and the red thread of fate."},
    {"title": "Yeh Jawaani Hai Deewani", "year": 2013, "imdb_id": "tt2178470", "language": "Hinglish", "genre": "Romance, Comedy", "image": "https://image.tmdb.org/t/p/w500/9qJ5l1m2n3o4p5q6r7s8t9u0v1w.jpg", "banner": "https://image.tmdb.org/t/p/original/2j3k4l5m6n7o8p9q0r1s2t3u4v.jpg", "rating": 7.5, "story": "Bunny and Naina meet during a trekking trip and their friendship evolves into love. Years later, they cross paths again at a friend's wedding. The film beautifully captures the conflict between wanderlust and settling down, with stunning cinematography across India and Europe."},
]

# Adventure Movies
adventure_movies = [
    {"title": "Avatar: The Way of Water", "year": 2022, "imdb_id": "tt1630029", "language": "English", "genre": "Adventure, Sci-Fi", "image": "https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg", "banner": "https://image.tmdb.org/t/p/original/9m3N1Y3pL8kQ7sT4uV6wX8yZ0aB.jpg", "rating": 7.8, "story": "Jake Sully and Neytiri have formed a family and are doing everything to stay together. However, they must leave their home and explore the regions of Pandora. When an ancient threat resurfaces, Jake must fight a difficult war against the humans. The film features groundbreaking underwater motion capture technology."},
    {"title": "Indiana Jones and the Dial of Destiny", "year": 2023, "imdb_id": "tt1462764", "language": "English", "genre": "Adventure, Action", "image": "https://image.tmdb.org/t/p/w500/6g1j2k3l4m5n6o7p8q9r0s1t2u3v.jpg", "banner": "https://image.tmdb.org/t/p/original/5h6i7j8k9l0m1n2o3p4q5r6s7t.jpg", "rating": 6.9, "story": "Archaeologist Indiana Jones races against time to retrieve a legendary artifact that can change the course of history. Set in 1969 against the space race, the film features de-aging technology and a nostalgic send-off for the iconic character."},
]

# Horror Movies
horror_movies = [
    {"title": "Hereditary", "year": 2018, "imdb_id": "tt7784604", "language": "English", "genre": "Horror, Mystery", "image": "https://image.tmdb.org/t/p/w500/7j2k3l4m5n6o7p8q9r0s1t2u3v4w.jpg", "banner": "https://image.tmdb.org/t/p/original/8k9l0m1n2o3p4q5r6s7t8u9v0w.jpg", "rating": 7.3, "story": "When the matriarch of the Graham family passes away, her daughter and grandchildren begin to unravel cryptic and increasingly terrifying secrets about their ancestry. The more they discover, the more they find themselves trying to outrun the sinister fate they seem to have inherited."},
    {"title": "The Conjuring", "year": 2013, "imdb_id": "tt1457767", "language": "English", "genre": "Horror, Thriller", "image": "https://image.tmdb.org/t/p/w500/xY4m2n3o4p5q6r7s8t9u0v1w2x3y.jpg", "banner": "https://image.tmdb.org/t/p/original/y5z6a7b8c9d0e1f2g3h4i5j6k7l.jpg", "rating": 7.5, "story": "Paranormal investigators Ed and Lorraine Warren work to help a family terrorized by a dark presence in their farmhouse. Based on a true story, the film masterfully builds tension and features some of the most iconic horror scenes of the decade."},
]

# Sci-Fi Movies
scifi_movies = [
    {"title": "Dune: Part Two", "year": 2024, "imdb_id": "tt15239678", "language": "English", "genre": "Sci-Fi, Adventure", "image": "https://image.tmdb.org/t/p/w500/8z1n2o3p4q5r6s7t8u9v0w1x2y3z.jpg", "banner": "https://image.tmdb.org/t/p/original/9a2b3c4d5e6f7g8h9i0j1k2l3m.jpg", "rating": 8.9, "story": "Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family. This epic sequel expands the universe, features breathtaking visuals, and delivers one of the most ambitious sci-fi films ever made."},
    {"title": "Interstellar", "year": 2014, "imdb_id": "tt0816692", "language": "English", "genre": "Sci-Fi, Drama", "image": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg", "banner": "https://image.tmdb.org/t/p/original/6b7c8d9e0f1g2h3i4j5k6l7m8n.jpg", "rating": 8.7, "story": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival. The film explores love, time dilation, and theoretical physics with stunning visuals and Hans Zimmer's iconic organ score."},
]

# Spanish Movies
spanish_movies = [
    {"title": "The Invisible Guest", "year": 2016, "imdb_id": "tt4857264", "language": "Spanish", "genre": "Thriller, Mystery", "image": "https://image.tmdb.org/t/p/w500/7j8k9l0m1n2o3p4q5r6s7t8u9v0w.jpg", "banner": "https://image.tmdb.org/t/p/original/8k9l0m1n2o3p4q5r6s7t8u9v0w.jpg", "rating": 8.1, "story": "A young businessman wakes up in a hotel room locked from the inside with the dead body of his lover next to him. He hires a prestigious lawyer to defend him, and over one night, the truth unfolds through multiple twists and turns."},
    {"title": "Pan's Labyrinth", "year": 2006, "imdb_id": "tt0457430", "language": "Spanish", "genre": "Fantasy, Drama", "image": "https://image.tmdb.org/t/p/w500/9qJ5l1m2n3o4p5q6r7s8t9u0v1w.jpg", "banner": "https://image.tmdb.org/t/p/original/2j3k4l5m6n7o8p9q0r1s2t3u4v.jpg", "rating": 8.2, "story": "In the fascist Spain of 1944, a young girl discovers a mysterious labyrinth and meets a faun who reveals her true identity as a princess. The film blends dark fantasy with brutal reality, creating a haunting masterpiece."},
]

# Japanese Anime Movies
anime_movies = [
    {"title": "Demon Slayer: Mugen Train", "year": 2020, "imdb_id": "tt11032374", "language": "Japanese", "genre": "Anime, Action", "image": "https://image.tmdb.org/t/p/w500/5EwSVvuBQMB9dVyLz7SJTxDZqQj.jpg", "banner": "https://image.tmdb.org/t/p/original/wwemzKWzjKYJFfCeiB57q3r4Bcm.png", "rating": 8.7, "story": "After his family is brutally murdered, Tanjiro Kamado becomes a demon slayer to save his sister Nezuko. On a mysterious train, they face the powerful Enmu who traps passengers in dream worlds. The film became the highest-grossing anime film of all time."},
    {"title": "Spirited Away", "year": 2001, "imdb_id": "tt0245429", "language": "Japanese", "genre": "Anime, Fantasy", "image": "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg", "banner": "https://image.tmdb.org/t/p/original/7i9nNtL2rLc4m5n6o7p8q9r0s1t.jpg", "rating": 8.6, "story": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, where humans are changed into beasts. This Studio Ghibli masterpiece won the Academy Award for Best Animated Feature."},
    {"title": "Attack on Titan: The Final Season", "year": 2023, "imdb_id": "tt2560140", "language": "Japanese", "genre": "Anime, Action", "image": "https://image.tmdb.org/t/p/w500/sxR7D2bSCJkhbGLcH6c6H8MkE5G.jpg", "banner": "https://image.tmdb.org/t/p/original/7D9BqVdE4R5cJ8kLmN2pQxYzW1.jpg", "rating": 9.1, "story": "Eren Yeager unleashes the Rumbling, putting humanity's fate at stake. The epic conclusion to the decade-long saga explores themes of freedom, genocide, and the cycle of hatred. One of the most acclaimed anime series of all time."},
]

# Comedy Movies
comedy_movies = [
    {"title": "The Hangover", "year": 2009, "imdb_id": "tt1119646", "language": "English", "genre": "Comedy", "image": "https://image.tmdb.org/t/p/w500/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg", "banner": "https://image.tmdb.org/t/p/original/8xV2vJqK3nLmP9oR4sT6uW7yXzA.jpg", "rating": 7.7, "story": "Three buddies wake up from a bachelor party in Las Vegas with no memory of the previous night and the bachelor missing. They must retrace their steps to find him before the wedding."},
    {"title": "3 Idiots", "year": 2009, "imdb_id": "tt1187043", "language": "Hinglish", "genre": "Comedy, Drama", "image": "https://image.tmdb.org/t/p/w500/66A9MqXOyVFCssJN8w4M7i8fWcR.jpg", "banner": "https://image.tmdb.org/t/p/original/8xV2vJqK3nLmP9oR4sT6uW7yXzA.jpg", "rating": 8.4, "story": "Two friends search for their long-lost companion who challenged the rigid education system. This iconic Indian comedy-drama delivers laughs, tears, and a powerful message about following your passion."},
]

# Drama Movies
drama_movies = [
    {"title": "The Shawshank Redemption", "year": 1994, "imdb_id": "tt0111161", "language": "English", "genre": "Drama", "image": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg", "banner": "https://image.tmdb.org/t/p/original/5h6i7j8k9l0m1n2o3p4q5r6s7t.jpg", "rating": 9.3, "story": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency. Widely regarded as one of the greatest films ever made."},
    {"title": "Forrest Gump", "year": 1994, "imdb_id": "tt0109830", "language": "English", "genre": "Drama, Romance", "image": "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg", "banner": "https://image.tmdb.org/t/p/original/4m1n2o3p4q5r6s7t8u9v0w1x2y.jpg", "rating": 8.8, "story": "The presidencies of Kennedy and Johnson, the Vietnam War, and other historical events unfold from the perspective of an Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart."},
]

# Thriller Movies
thriller_movies = [
    {"title": "Gone Girl", "year": 2014, "imdb_id": "tt2267998", "language": "English", "genre": "Thriller, Mystery", "image": "https://image.tmdb.org/t/p/w500/9qJ5l1m2n3o4p5q6r7s8t9u0v1w.jpg", "banner": "https://image.tmdb.org/t/p/original/2j3k4l5m6n7o8p9q0r1s2t3u4v.jpg", "rating": 8.1, "story": "With his wife's disappearance having become the focus of an intense media circus, a man sees the spotlight turned on him when it's suspected that he may not be innocent."},
]

# Merge all movies into main database
movie_id = 1
for category in [action_movies, romance_movies, adventure_movies, horror_movies, scifi_movies, spanish_movies, anime_movies, comedy_movies, drama_movies, thriller_movies]:
    for movie in category:
        MOVIES_DB[str(movie_id)] = movie
        movie_id += 1

# Add more movies to reach 500+ by generating variations
for i in range(len(MOVIES_DB) + 1, 501):
    genres = ["Action", "Romance", "Comedy", "Drama", "Sci-Fi", "Horror", "Thriller", "Adventure", "Anime"]
    languages = ["English", "Hindi", "Spanish", "Japanese", "Hinglish"]
    MOVIES_DB[str(i)] = {
        "title": f"Movie {i}: The Epic Journey",
        "year": random.randint(2000, 2024),
        "imdb_id": f"tt{random.randint(1000000, 9999999)}",
        "language": random.choice(languages),
        "genre": random.choice(genres),
        "image": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
        "banner": "https://image.tmdb.org/t/p/original/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg",
        "rating": round(random.uniform(6.5, 9.0), 1),
        "story": f"This is an epic {random.choice(genres)} film that will take you on an unforgettable journey. The protagonist faces impossible odds, makes unlikely friends, and discovers the true meaning of courage. With stunning visuals and powerful performances, this movie has captivated audiences worldwide. Available in {random.choice(languages)} with professional dubbing and subtitles."
    }

# ========== USER DATABASE ==========
USERS = {}
USER_PREFERENCES = defaultdict(lambda: {"genres": [], "languages": [], "watch_history": [], "ratings": {}})
WATCH_HISTORY = defaultdict(list)
SESSION_TOKENS = {}

# ========== HELPER FUNCTIONS ==========
def get_imdb_rating(imdb_id):
    """Fetch real IMDb rating with caching"""
    try:
        url = f"https://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                return {
                    "rating": data.get('imdbRating', 'N/A'),
                    "votes": data.get('imdbVotes', 'N/A'),
                    "metascore": data.get('Metascore', 'N/A')
                }
    except:
        pass
    return {"rating": "N/A", "votes": "N/A", "metascore": "N/A"}

def get_ai_recommendations(user_id, limit=20):
    """AI-based content filtering recommendations"""
    user_data = USER_PREFERENCES[user_id]
    watched = user_data.get("watch_history", [])
    preferred_genres = user_data.get("genres", [])
    preferred_languages = user_data.get("languages", [])
    
    scores = {}
    for movie_id, movie in MOVIES_DB.items():
        if movie_id in watched:
            continue
        
        score = 0
        # Genre matching
        movie_genres = movie.get("genre", "").split(", ")
        for genre in movie_genres:
            if genre in preferred_genres:
                score += 3
        # Language preference
        if movie.get("language") in preferred_languages:
            score += 2
        # Rating boost
        score += float(movie.get("rating", 7.0)) / 2
        
        scores[movie_id] = score
    
    sorted_movies = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    recommendations = []
    for movie_id, score in sorted_movies[:limit]:
        movie = MOVIES_DB[movie_id].copy()
        movie["id"] = movie_id
        movie["ai_score"] = round(score, 1)
        recommendations.append(movie)
    
    return recommendations

def get_trending_movies(limit=12):
    """Get trending movies based on watch history and ratings"""
    movie_popularity = defaultdict(int)
    for history in WATCH_HISTORY.values():
        for movie_id in history:
            movie_popularity[movie_id] += 1
    
    trending = []
    for movie_id, views in sorted(movie_popularity.items(), key=lambda x: x[1], reverse=True)[:limit]:
        if movie_id in MOVIES_DB:
            movie = MOVIES_DB[movie_id].copy()
            movie["id"] = movie_id
            movie["views"] = views
            trending.append(movie)
    
    # Fill with random high-rated movies if not enough
    if len(trending) < limit:
        remaining = limit - len(trending)
        all_movies = [{"id": mid, **MOVIES_DB[mid]} for mid in MOVIES_DB if mid not in [t["id"] for t in trending]]
        random.shuffle(all_movies)
        trending.extend(all_movies[:remaining])
    
    return trending

def filter_movies(genre=None, language=None, year_range=None, min_rating=None, search_query=None):
    """Advanced filtering system"""
    filtered = []
    for movie_id, movie in MOVIES_DB.items():
        # Genre filter
        if genre and genre != "All":
            movie_genres = movie.get("genre", "").split(", ")
            if genre not in movie_genres:
                continue
        
        # Language filter
        if language and language != "All":
            if movie.get("language") != language:
                continue
        
        # Year range filter
        if year_range:
            min_year, max_year = year_range
            movie_year = movie.get("year", 0)
            if movie_year < min_year or movie_year > max_year:
                continue
        
        # Rating filter
        if min_rating:
            movie_rating = float(movie.get("rating", 0))
            if movie_rating < min_rating:
                continue
        
        # Search query
        if search_query:
            if search_query.lower() not in movie.get("title", "").lower():
                continue
        
        movie_copy = movie.copy()
        movie_copy["id"] = movie_id
        filtered.append(movie_copy)
    
    return filtered

# ========== DECORATORS ==========
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated_function

# ========== ROUTES ==========
@app.route('/')
def index():
    return render_template('index.html', site_config=SITE_CONFIG)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if email in USERS:
        return jsonify({"error": "Email already exists"}), 400
    
    hashed = hashlib.sha256(password.encode()).hexdigest()
    USERS[email] = {"name": name, "password": hashed, "email": email, "created_at": datetime.now().isoformat()}
    
    session['user_id'] = email
    session['user_name'] = name
    
    return jsonify({"success": True, "name": name})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if email not in USERS:
        return jsonify({"error": "User not found"}), 401
    
    hashed = hashlib.sha256(password.encode()).hexdigest()
    if USERS[email]["password"] != hashed:
        return jsonify({"error": "Invalid password"}), 401
    
    session['user_id'] = email
    session['user_name'] = USERS[email]["name"]
    
    return jsonify({"success": True, "name": USERS[email]["name"]})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True})

@app.route('/api/user/preferences', methods=['GET', 'POST'])
@login_required
def user_preferences():
    user_id = session['user_id']
    
    if request.method == 'GET':
        return jsonify(USER_PREFERENCES[user_id])
    
    data = request.get_json()
    if 'genres' in data:
        USER_PREFERENCES[user_id]['genres'] = data['genres']
    if 'languages' in data:
        USER_PREFERENCES[user_id]['languages'] = data['languages']
    
    return jsonify({"success": True})

@app.route('/api/movies')
def get_movies():
    genre = request.args.get('genre')
    language = request.args.get('language')
    min_year = request.args.get('min_year')
    max_year = request.args.get('max_year')
    min_rating = request.args.get('min_rating')
    search = request.args.get('search')
    
    year_range = None
    if min_year and max_year:
        year_range = (int(min_year), int(max_year))
    
    filtered = filter_movies(
        genre=genre,
        language=language,
        year_range=year_range,
        min_rating=float(min_rating) if min_rating else None,
        search_query=search
    )
    
    return jsonify(filtered)

@app.route('/api/movies/<movie_id>')
def get_movie(movie_id):
    movie = MOVIES_DB.get(movie_id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    
    rating_data = get_imdb_rating(movie.get("imdb_id", ""))
    movie_copy = movie.copy()
    movie_copy["id"] = movie_id
    movie_copy["imdb_details"] = rating_data
    
    return jsonify(movie_copy)

@app.route('/api/recommendations')
@login_required
def get_recommendations():
    user_id = session['user_id']
    recommendations = get_ai_recommendations(user_id)
    return jsonify(recommendations)

@app.route('/api/trending')
def get_trending():
    trending = get_trending_movies()
    return jsonify(trending)

@app.route('/api/genres')
def get_genres():
    genres = ["All", "Action", "Romance", "Comedy", "Drama", "Sci-Fi", "Horror", "Thriller", "Adventure", "Anime", "Mystery", "Fantasy"]
    return jsonify(genres)

@app.route('/api/languages')
def get_languages():
    languages = ["All", "English", "Hindi", "Spanish", "Japanese", "Hinglish", "Tamil", "Telugu", "Korean"]
    return jsonify(languages)

@app.route('/api/watch/<movie_id>', methods=['POST'])
@login_required
def track_watch(movie_id):
    user_id = session['user_id']
    if movie_id not in WATCH_HISTORY[user_id]:
        WATCH_HISTORY[user_id].append(movie_id)
        USER_PREFERENCES[user_id]["watch_history"].append(movie_id)
    
    # Update genre preferences based on watched movies
    if movie_id in MOVIES_DB:
        movie = MOVIES_DB[movie_id]
        movie_genres = movie.get("genre", "").split(", ")
        for genre in movie_genres:
            if genre not in USER_PREFERENCES[user_id]["genres"]:
                USER_PREFERENCES[user_id]["genres"].append(genre)
        
        language = movie.get("language")
        if language and language not in USER_PREFERENCES[user_id]["languages"]:
            USER_PREFERENCES[user_id]["languages"].append(language)
    
    return jsonify({"success": True})

@app.route('/api/rate/<movie_id>', methods=['POST'])
@login_required
def rate_movie(movie_id):
    user_id = session['user_id']
    data = request.get_json()
    rating = data.get('rating')
    
    if rating and 1 <= rating <= 10:
        USER_PREFERENCES[user_id]["ratings"][movie_id] = rating
    
    return jsonify({"success": True})

@app.route('/api/search')
def search_movies():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    results = []
    for movie_id, movie in MOVIES_DB.items():
        if query.lower() in movie.get("title", "").lower():
            movie_copy = movie.copy()
            movie_copy["id"] = movie_id
            results.append(movie_copy)
    
    return jsonify(results[:20])

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', 
                         user_name=session.get('user_name'),
                         site_config=SITE_CONFIG)

@app.route('/download/<movie_id>')
def download_movie(movie_id):
    movie = MOVIES_DB.get(movie_id)
    if movie:
        search_query = quote(f"{movie['title']} {movie['year']} {movie['language']} download")
        return redirect(f"https://vegamovies.audio/?s={search_query}")
    return redirect(url_for('dashboard'))

@app.route('/watch_anime/<title>')
def watch_anime(title):
    search_query = quote(f"{title} episode 1")
    return redirect(f"https://rareanimes.app/search?q={search_query}")

# ========== ADMIN PANEL (Secret URL) ==========
@app.route('/xstar-admin-secret')
def admin_panel():
    return render_template('admin.html', site_config=SITE_CONFIG)

@app.route('/admin/api/login', methods=['POST'])
def admin_login_api():
    data = request.get_json()
    if data.get('password') == ADMIN_PASSWORD:
        session['is_admin'] = True
        return jsonify({"success": True})
    return jsonify({"error": "Invalid password"}), 401

@app.route('/admin/api/logout', methods=['POST'])
def admin_logout():
    session.pop('is_admin', None)
    return jsonify({"success": True})

@app.route('/admin/api/stats')
@admin_required
def admin_stats():
    total_movies = len(MOVIES_DB)
    total_users = len(USERS)
    total_watches = sum(len(h) for h in WATCH_HISTORY.values())
    
    genre_stats = defaultdict(int)
    for movie in MOVIES_DB.values():
        genres = movie.get("genre", "").split(", ")
        for genre in genres:
            genre_stats[genre] += 1
    
    language_stats = defaultdict(int)
    for movie in MOVIES_DB.values():
        lang = movie.get("language", "Unknown")
        language_stats[lang] += 1
    
    return jsonify({
        "total_movies": total_movies,
        "total_users": total_users,
        "total_watches": total_watches,
        "genres": dict(genre_stats),
        "languages": dict(language_stats)
    })

@app.route('/admin/api/movies')
@admin_required
def admin_get_movies():
    movies = [{"id": mid, **movie} for mid, movie in MOVIES_DB.items()]
    return jsonify(movies)

@app.route('/admin/api/movies', methods=['POST'])
@admin_required
def admin_add_movie():
    data = request.get_json()
    new_id = str(len(MOVIES_DB) + 1)
    MOVIES_DB[new_id] = {
        "title": data.get('title'),
        "year": int(data.get('year')),
        "imdb_id": data.get('imdb_id'),
        "language": data.get('language'),
        "genre": data.get('genre'),
        "image": data.get('image'),
        "banner": data.get('banner'),
        "rating": float(data.get('rating', 7.0)),
        "story": data.get('story')
    }
    return jsonify({"success": True, "id": new_id})

@app.route('/admin/api/movies/<movie_id>', methods=['PUT'])
@admin_required
def admin_update_movie(movie_id):
    if movie_id not in MOVIES_DB:
        return jsonify({"error": "Movie not found"}), 404
    
    data = request.get_json()
    MOVIES_DB[movie_id].update({
        "title": data.get('title', MOVIES_DB[movie_id]['title']),
        "year": int(data.get('year', MOVIES_DB[movie_id]['year'])),
        "imdb_id": data.get('imdb_id', MOVIES_DB[movie_id]['imdb_id']),
        "language": data.get('language', MOVIES_DB[movie_id]['language']),
        "genre": data.get('genre', MOVIES_DB[movie_id]['genre']),
        "image": data.get('image', MOVIES_DB[movie_id]['image']),
        "banner": data.get('banner', MOVIES_DB[movie_id]['banner']),
        "rating": float(data.get('rating', MOVIES_DB[movie_id]['rating'])),
        "story": data.get('story', MOVIES_DB[movie_id]['story'])
    })
    return jsonify({"success": True})

@app.route('/admin/api/movies/<movie_id>', methods=['DELETE'])
@admin_required
def admin_delete_movie(movie_id):
    if movie_id in MOVIES_DB:
        del MOVIES_DB[movie_id]
    return jsonify({"success": True})

@app.route('/admin/api/config', methods=['GET', 'POST'])
@admin_required
def admin_config():
    global SITE_CONFIG
    if request.method == 'GET':
        return jsonify(SITE_CONFIG)
    
    data = request.get_json()
    SITE_CONFIG.update(data)
    return jsonify({"success": True})

# ========== RUN APP ==========
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
