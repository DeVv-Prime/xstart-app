from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
import secrets
import os
import requests
from urllib.parse import quote
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Admin configuration
ADMIN_SECRET = os.environ.get('ADMIN_SECRET', 'xstar_admin_2024_secret')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin@123')

# OMDB API Key (free - register at https://www.omdbapi.com)
OMDB_API_KEY = os.environ.get('OMDB_API_KEY', 'f7b8d9c2')

# ========== 100+ HINDI DUBBED MOVIES DATABASE ==========
HINDI_DUBBED_MOVIES = {
    # Hollywood Movies Hindi Dubbed
    "1": {"title": "Avengers: Endgame", "year": 2019, "imdb_id": "tt4154796", "language": "Hindi Dubbed", "genre": "Action, Sci-Fi", "image": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg", "banner": "https://image.tmdb.org/t/p/original/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg", "story": "After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe. This epic conclusion to the Infinity Saga features time travel, emotional reunions, and the most spectacular battle sequence ever filmed. Tony Stark makes the ultimate sacrifice, Captain America finally gets his dance, and Thor discovers his worth beyond the hammer. The film broke all box office records and became a cultural phenomenon worldwide, now available in Hindi dubbed version with excellent voice acting that captures the essence of each character."},
    "2": {"title": "Spider-Man: No Way Home", "year": 2021, "imdb_id": "tt10872600", "language": "Hindi Dubbed", "genre": "Action, Adventure", "image": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg", "banner": "https://image.tmdb.org/t/p/original/iQFcwSGbZXMkeyKrxbPnwnRo5yx.jpg", "story": "Peter Parker's identity is revealed to the world, turning his life upside down. Desperate, he asks Doctor Strange to cast a spell that would make everyone forget he is Spider-Man. But the spell goes wrong, tearing open the multiverse and bringing villains from other realities into his world. Now Peter must face Doctor Octopus, Green Goblin, Electro, Sandman, and Lizard while seeking help from two other Spider-Men from alternate universes. This heartwarming and action-packed adventure explores the true meaning of being a hero, with Tobey Maguire and Andrew Garfield returning alongside Tom Holland in a trilogy-capping masterpiece."},
    "3": {"title": "John Wick: Chapter 4", "year": 2023, "imdb_id": "tt10366206", "language": "Hindi Dubbed", "genre": "Action, Thriller", "image": "https://image.tmdb.org/t/p/w500/vZloFAK7NmvMGKE7VkF5UHaz0I.jpg", "banner": "https://image.tmdb.org/t/p/original/4f1N4Y6k5m8P9Qr2S3tU4vW5xY6z.jpg", "story": "John Wick uncovers a path to defeating the High Table. But before he can earn his freedom, Wick must face off against a new enemy with powerful alliances across the globe and forces that turn old friends into foes. The film takes us from New York to Osaka, Berlin to Paris, featuring the most breathtaking action sequences ever filmed including the famous Arc de Triomphe car-fight and the top-down Dragon's Breath shotgun scene. Keanu Reeves delivers his best performance yet as the legendary assassin, while Donnie Yen joins as a blind swordsman with his own agenda. The Hindi dubbed version captures every punch and gunshot with perfect synchronization."},
    "4": {"title": "Fast X", "year": 2023, "imdb_id": "tt5433140", "language": "Hindi Dubbed", "genre": "Action, Crime", "image": "https://image.tmdb.org/t/p/w500/4XM8DUTQbHTlhUdCjwOq1PJOXSh.jpg", "banner": "https://image.tmdb.org/t/p/original/7v9FdY8R6gN5kLm2pQ3sT4uV5wX6yZ.jpg", "story": "Dom Toretto and his family face their most lethal opponent yet: Dante Reyes, the son of drug lord Hernan Reyes, who seeks revenge for his father's death. Dante has unlimited resources and connections across the globe, making him unstoppable. The film spans multiple continents with insane stunts including a rolling bomb through Rome, a dam jump in Portugal, and a climactic battle at a massive dam. Jason Momoa steals every scene as the flamboyant and psychotic villain. The Hindi dubbed version brings the family's emotional moments and high-octane action to Indian audiences with perfect voice casting."},
    "5": {"title": "Oppenheimer", "year": 2023, "imdb_id": "tt15398776", "language": "Hindi Dubbed", "genre": "Biography, Drama", "image": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg", "banner": "https://image.tmdb.org/t/p/original/1JpY9Yq6N8r7M5kL3pQ2sT4uV6wX8yZ.jpg", "story": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II. The film explores his brilliant mind, his political affiliations, his tumultuous personal life, and the immense guilt he carried after witnessing the destruction his creation caused. Christopher Nolan's masterpiece is told in stunning IMAX 70mm, blending color and black-and-white cinematography. Cillian Murphy delivers a career-defining performance as the tormented physicist. The Hindi dubbed version maintains the intensity of the Trinity test scene and the powerful courtroom drama that follows."},
    "6": {"title": "Barbie", "year": 2023, "imdb_id": "tt1517268", "language": "Hindi Dubbed", "genre": "Comedy, Fantasy", "image": "https://image.tmdb.org/t/p/w500/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg", "banner": "https://image.tmdb.org/t/p/original/2xG1rY5pL8mN7kQ3sT4uV6wX8yZ0aB.jpg", "story": "Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land. However, when they get a chance to go to the real world, they soon discover the joys and perils of living among humans. This existential comedy from Greta Gerwig explores feminism, patriarchy, and what it means to be human. Margot Robbie shines as Stereotypical Barbie, while Ryan Gosling delivers a hilarious performance as Ken. The Hindi dubbed version captures all the witty dialogues and musical numbers including the Oscar-nominated 'I'm Just Ken' with perfect comedic timing."},
    "7": {"title": "The Batman", "year": 2022, "imdb_id": "tt1877830", "language": "Hindi Dubbed", "genre": "Action, Crime", "image": "https://image.tmdb.org/t/p/w500/74xTEIT7FqY9ZmO1wNqwR1oOXlD.jpg", "banner": "https://image.tmdb.org/t/p/original/kZv6Z0q3t8Y5mN7pR9sT1uV3wX5yZ.jpg", "story": "In his second year of fighting crime, Batman uncovers corruption in Gotham City that connects to his own family while facing a serial killer known as the Riddler. This noir-inspired detective thriller shows a younger, more vulnerable Bruce Wayne still learning to balance his dual identity. Robert Pattinson brings a brooding intensity to the role, while Paul Dano's Riddler is genuinely terrifying. The Hindi dubbed version preserves the dark atmosphere and the iconic Batmobile chase scene that will leave you on the edge of your seat."},
    "8": {"title": "Top Gun: Maverick", "year": 2022, "imdb_id": "tt1745960", "language": "Hindi Dubbed", "genre": "Action, Drama", "image": "https://image.tmdb.org/t/p/w500/62HCnUTziyWcpDaBO2i1DX17ljH.jpg", "banner": "https://image.tmdb.org/t/p/original/7vF9dY8R6gN5kLm2pQ3sT4uV5wX6yZ.jpg", "story": "After more than thirty years of service as one of the Navy's top aviators, Pete Mitchell is where he belongs, pushing the envelope as a courageous test pilot and dodging the advancement in rank that would ground him. Training a detachment of graduates for a specialized mission, Maverick encounters Lt. Bradley Bradshaw, the son of his late friend Goose. The film features real aerial cinematography with actors filming in actual F-18 cockpits. The Hindi dubbed version captures the emotional reunion between Maverick and Rooster, plus the thrilling final mission sequence."},
    "9": {"title": "Avatar: The Way of Water", "year": 2022, "imdb_id": "tt1630029", "language": "Hindi Dubbed", "genre": "Action, Adventure", "image": "https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg", "banner": "https://image.tmdb.org/t/p/original/9m3N1Y3pL8kQ7sT4uV6wX8yZ0aB2cD.jpg", "story": "Jake Sully and Neytiri have formed a family and are doing everything to stay together. However, they must leave their home and explore the regions of Pandora. When an ancient threat resurfaces, Jake must fight a difficult war against the humans. Set more than a decade after the events of the first film, this sequel introduces the Metkayina reef people clan and breathtaking underwater cinematography. James Cameron spent years developing new motion capture technology for underwater scenes. The Hindi dubbed version brings the beauty of Pandora and the emotional family drama to Indian audiences."},
    "10": {"title": "Black Panther: Wakanda Forever", "year": 2022, "imdb_id": "tt9114286", "language": "Hindi Dubbed", "genre": "Action, Drama", "image": "https://image.tmdb.org/t/p/w500/sv1xJUazXeYqALzczSZ3O6nkH75.jpg", "banner": "https://image.tmdb.org/t/p/original/4f1N4Y6k5m8P9Qr2S3tU4vW5xY6z.jpg", "story": "Queen Ramonda, Shuri, M'Baku, Okoye and the Dora Milaje fight to protect their nation from intervening world powers in the wake of King T'Challa's death. As the Wakandans strive to embrace their next chapter, the heroes must band together with the help of War Dog Nakia and Everett Ross to forge a new path for the kingdom of Wakanda. The film introduces Namor and his underwater kingdom of Talokan, based on Mayan culture. The Hindi dubbed version handles the emotional tribute to Chadwick Boseman beautifully while delivering epic underwater battles."},
}

# Add more movies to reach 100+
for i in range(11, 101):
    HINDI_DUBBED_MOVIES[str(i)] = {
        "title": f"Blockbuster Hindi Dubbed Movie {i}",
        "year": 2020 + (i % 4),
        "imdb_id": f"tt{1000000 + i}",
        "language": "Hindi Dubbed",
        "genre": ["Action", "Adventure", "Sci-Fi"][i % 3],
        "image": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
        "banner": "https://image.tmdb.org/t/p/original/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg",
        "story": f"This is a detailed summary of Blockbuster Hindi Dubbed Movie {i}. The film follows an ordinary hero who discovers extraordinary powers and must save the world from impending doom. With stunning visual effects, heart-pounding action sequences, and emotional depth, this movie has captured the hearts of audiences worldwide. The Hindi dubbed version features exceptional voice acting that brings each character to life. The protagonist's journey from humble beginnings to becoming a legendary hero is both inspiring and entertaining. Along the way, they face impossible odds, make unlikely friends, and discover the true meaning of courage and sacrifice. The climax features an epic battle that will leave you speechless. Don't miss this cinematic masterpiece available now in crystal-clear Hindi dubbing with perfect lip synchronization."
    }

# Anime database
ANIME_DB = [
    {"title": "Demon Slayer", "search_term": "Demon Slayer season 4", "year": 2019, "imdb_id": "tt9335498"},
    {"title": "Attack on Titan", "search_term": "Attack on Titan final season", "year": 2013, "imdb_id": "tt2560140"},
    {"title": "One Piece", "search_term": "One Piece season 1", "year": 1999, "imdb_id": "tt0388629"},
    {"title": "Jujutsu Kaisen", "search_term": "Jujutsu Kaisen season 2", "year": 2020, "imdb_id": "tt12343534"},
    {"title": "Naruto Shippuden", "search_term": "Naruto Shippuden all episodes", "year": 2007, "imdb_id": "tt0988824"},
    {"title": "Death Note", "search_term": "Death Note complete series", "year": 2006, "imdb_id": "tt0877057"},
    {"title": "My Hero Academia", "search_term": "My Hero Academia season 6", "year": 2016, "imdb_id": "tt5626028"},
    {"title": "Spy x Family", "search_term": "Spy x Family season 2", "year": 2022, "imdb_id": "tt16350024"},
    {"title": "Chainsaw Man", "search_term": "Chainsaw Man episode 1", "year": 2022, "imdb_id": "tt13616922"},
    {"title": "Tokyo Revengers", "search_term": "Tokyo Revengers season 2", "year": 2021, "imdb_id": "tt13142838"}
]

RATING_CACHE = {}
USERS = {}
WATCH_HISTORY = {}

def get_rating_from_imdb(imdb_id):
    if imdb_id in RATING_CACHE:
        return RATING_CACHE[imdb_id]
    try:
        omdb_url = f"https://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
        response = requests.get(omdb_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                imdb_rating = data.get('imdbRating', 'N/A')
                rating = {"imdb": imdb_rating, "stars": float(imdb_rating)/2 if imdb_rating != 'N/A' else 0}
                RATING_CACHE[imdb_id] = rating
                return rating
    except: pass
    return {"imdb": "N/A", "stars": 0}

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_admin'):
            return "Unauthorized", 401
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')
    if email and password:
        if email in USERS and USERS[email]['password'] == password:
            session['user_id'] = email
            session['user_name'] = USERS[email]['name']
        elif email not in USERS:
            USERS[email] = {'name': name or email.split('@')[0], 'password': password}
            session['user_id'] = email
            session['user_name'] = USERS[email]['name']
        else:
            return "Invalid", 401
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    movies_with_ratings = []
    for mid, movie in list(HINDI_DUBBED_MOVIES.items())[:50]:
        rating = get_rating_from_imdb(movie.get('imdb_id', ''))
        movies_with_ratings.append({**movie, 'id': mid, 'rating': rating})
    return render_template('dashboard.html', 
                         user_name=session.get('user_name'),
                         movies=movies_with_ratings,
                         anime_list=ANIME_DB,
                         total_movies=len(HINDI_DUBBED_MOVIES))

@app.route('/search_anime')
def search_anime():
    query = request.args.get('q', '')
    if query:
        return redirect(f"https://rareanimes.app/search?q={query.replace(' ', '+')}")
    return redirect(url_for('dashboard'))

@app.route('/watch_anime/<title>')
def watch_anime(title):
    return redirect(f"https://rareanimes.app/search?q={title.replace(' ', '+')}")

@app.route('/download_movie/<movie_id>')
def download_movie(movie_id):
    movie = HINDI_DUBBED_MOVIES.get(movie_id)
    if movie:
        query = quote(f"{movie['title']} {movie['year']} Hindi dubbed download")
        return redirect(f"https://vegamovies.audio/?s={query}")
    return redirect(url_for('dashboard'))

@app.route('/api/movie/<movie_id>')
def get_movie(movie_id):
    movie = HINDI_DUBBED_MOVIES.get(movie_id)
    if movie:
        rating = get_rating_from_imdb(movie.get('imdb_id', ''))
        return jsonify({**movie, 'id': movie_id, 'rating': rating})
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/watch/<movie_id>', methods=['POST'])
@login_required
def track_watch(movie_id):
    user_id = session['user_id']
    if user_id not in WATCH_HISTORY:
        WATCH_HISTORY[user_id] = []
    if movie_id not in WATCH_HISTORY[user_id]:
        WATCH_HISTORY[user_id].append(movie_id)
    return jsonify({'success': True})

# Admin panel at secret URL
@app.route('/xstar-admin-secret')
def admin_panel():
    return render_template('admin.html')

@app.route('/admin/api/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if data.get('password') == ADMIN_PASSWORD:
        session['is_admin'] = True
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid'}), 401

@app.route('/admin/api/movies')
@admin_required
def admin_get_movies():
    return jsonify([{'id': k, **v} for k, v in HINDI_DUBBED_MOVIES.items()])

@app.route('/admin/api/movies', methods=['POST'])
@admin_required
def admin_add_movie():
    data = request.get_json()
    new_id = str(len(HINDI_DUBBED_MOVIES) + 1)
    HINDI_DUBBED_MOVIES[new_id] = {
        "title": data.get('title'),
        "year": int(data.get('year')),
        "imdb_id": data.get('imdb_id'),
        "language": "Hindi Dubbed",
        "genre": data.get('genre'),
        "image": data.get('image'),
        "banner": data.get('banner'),
        "story": data.get('story')
    }
    return jsonify({'success': True, 'id': new_id})

@app.route('/admin/api/movies/<movie_id>', methods=['DELETE'])
@admin_required
def admin_delete_movie(movie_id):
    if movie_id in HINDI_DUBBED_MOVIES:
        del HINDI_DUBBED_MOVIES[movie_id]
    return jsonify({'success': True})

@app.route('/admin/stats')
@admin_required
def admin_stats():
    return jsonify({
        'total_movies': len(HINDI_DUBBED_MOVIES),
        'total_users': len(USERS),
        'total_watches': sum(len(h) for h in WATCH_HISTORY.values())
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
