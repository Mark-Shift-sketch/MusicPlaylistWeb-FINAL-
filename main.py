from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import re
from datetime import datetime, timedelta
from flask import jsonify, request
from flask_migrate import Migrate





app = Flask(__name__)
app.secret_key = 'alkxctcegjjdvfbvgxzc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

def insert_music_data():
    for song_data in MUSIC_FILES:  # Use the correct variable name
        exists = Music.query.filter_by(title=song_data['title']).first()
        if not exists:
            new_song = Music(**song_data)
            db.session.add(new_song)
    db.session.commit()

MUSIC_FILES = [
        {
            "title": "Stairway To Heaven",
            "artist": "Led Zeppelin",
            "genre": "Rock",
            "file": "music/StairwayToHeaven.mp3"
        },
        {
            "title": "Shape of You",
            "artist": "Ed Sheeran",
            "genre": "Pop",
            "file": "music/ShapeofYou.mp3"
        },
        {
            "title": "Lose Yourself",
            "artist": "Eminem",
            "genre": "Rock",
            "file": "music/LoseYourself.mp3"
        },
        {
            "title": "Take Five",
            "artist": "Dave Brubeck",
            "genre": "Jazz",
            "file": "music/TakeFive.mp3"
        },
        {
            "title": "My Favorite Things from The Sound of Music",
            "artist": "Dave Brubeck",
            "genre": "Jazz",
            "file": "music/MyFavoriteThingsfromTheSoundofMusic(Official HD Video).mp3"
        },
        {
            "title": "Smells Like Teen Spirit",
            "artist": "Dave Brubeck",
            "genre": "Rock",
            "file": "music/NirvanaSmellsLikeTeenSpirit(Lyrics).mp3"
        },
        {
            "title": "So What",
            "artist": "Dave Brubeck",
            "genre": "Jazz",
            "file": "music/P!nkSoWhat(Official Video).mp3"
        },
        {
            "title": "Queen",
            "artist": "Bohemian Rhapsody",
            "genre": "Rock",
            "file": "music/QueenBohemianRhapsody(Official Video Remastered).mp3"
        },
        {
            "title": "Rolling In The Deep And Set Fire To The Rain",
            "artist": "Adele",
            "genre": "Pop",
            "file": "music/RollingInTheDeepAdele(Lyrics)SetFireToTheRainAdele(Lyrics).mp3"
        },
        {
            "title": "Moonlight Sonata",
            "artist": "Beethoven",
            "genre": "Classical",
            "file": "music/BeethovenMoonlightSonata(1st Movement).mp3"
        },
        {
            "title": "Canon In D",
            "artist": "Pachelbel",
            "genre": "Classical",
            "file": "music/CanoninDPachelbel.mp3"
        },
        {
            "title": "Hotels California",
            "artist": "Dave Brubeck",
            "genre": "Rock",
            "file": "music/EaglesHotelCalifornia(Live 1977)(Official Video)[HD].mp3"
        },
        {
            "title": "Sweet Child O Mine",
            "artist": "Gun N' Poses",
            "genre": "Rock",
            "file": "music/GunsNRosesSweetChildOMine(Lyrics).mp3"
        },
        {
            "title": "Like A Player",
            "artist": "Madonna",
            "genre": "Pop",
            "file": "music/MadonnaLikeAPrayer(Lyrics).mp3"
        },
        {
            "title": "Thriller",
            "artist": "Micheal Jackson",
            "genre": "Pop",
            "file": "music/MichaelJacksonThriller(Lyrics).mp3"
        },
        {
            "title": "All Blues",
            "artist": "Miles Bavis",
            "genre": "Jazz",
            "file": "music/MilesDavisAllBlues(Official Audio).mp3"
        },
        {
            "title": "Blue In Green",
            "artist": "Miles Davis",
            "genre": "Jazz",
            "file": "music/MilesDavisBlueInGreen(Official Audio).mp3"
        },
        {
            "title": "My Favorite Things from The Soud of Music",
            "artist": "unknow",
            "genre": "Jazz",
            "file": "music/MyFavoriteThingsfromTheSoundofMusic(Official HD Video).mp3"
        },
        {
            "title": "The Weeknd",
            "artist": "Blinding Lights",
            "genre": "Pop",
            "file": "music/TheWeekndBlindingLights(Lyrics).mp3"
        },
    ]


class Music(db.Model):
    __tablename__ = 'music_files'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    file = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Music {self.title} by {self.artist}>'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_banned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Add cascading delete to relationships
    friendships = db.relationship('Friendship', foreign_keys='Friendship.user_id', cascade="all, delete-orphan")

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    file = db.Column(db.String, nullable=False)


class Shared(db.Model):
    __tablename__ = 'shared'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String, nullable=False)
    receiver = db.Column(db.String, nullable=False)
    content_type = db.Column(db.String, nullable=False)  # 'song' or 'genre'
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Friendship(db.Model):
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', foreign_keys=[user_id], backref='friends')
    friend = db.relationship('User', foreign_keys=[friend_id])



class Update(db.Model):
    __tablename__ = 'updates'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    reporter = db.Column(db.String, nullable=False)
    content_type = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    reason = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
class PlaylistSong(db.Model):
    __tablename__ = 'playlist_songs'
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)

class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_group = db.Column(db.Boolean, default=False)

    # Define relationship with backref
    user = db.relationship('User', backref=db.backref('playlists', lazy=True, cascade="all, delete-orphan"))


class GroupMember(db.Model):
    __tablename__ = 'group_member'

    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))  #  match Playlist table name
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))          #  match User table name



@app.before_request
def initialize_database():
    db.create_all()
    insert_music_data()  # Add this line
    populate_songs_db()  # 
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', password='password')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created")


def get_user_id(username):
    user = User.query.filter_by(username=username).first()
    return user.id if user else None


def get_songs():
    songs = Song.query.all()
    return [{"id": s.id, "title": s.title, "artist": s.artist, "genre": s.genre, "file": s.file} for s in songs]

def get_playlists(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return {}

    playlists = {}
    for pl in user.playlists:
        song_entries = PlaylistSong.query.filter_by(playlist_id=pl.id).all()
        songs = [Song.query.get(se.song_id) for se in song_entries]
        playlists[pl.name] = [{"id": s.id, "title": s.title, "artist": s.artist, "genre": s.genre, "file": s.file} for s in songs]
    return playlists


def populate_songs_db():
    for song in MUSIC_FILES:
        exists = Song.query.filter_by(title=song['title'], artist=song['artist']).first()
        if not exists:
            new_song = Song(title=song['title'], artist=song['artist'], genre=song['genre'], file=song['file'])
            db.session.add(new_song)
    db.session.commit()


@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email'].strip()
        username = request.form['username'].strip()
        password = request.form['password']
        confirm_password = request.form.get('confirm_password')
        
        if not confirm_password:
            return "Confirm password field is missing!"
        
        if not re.match(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", email):
            return render_template("signup.html", message="Invalid email address")
        
        supported_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'phinmaed.com']
        if email.split('@')[1] not in supported_domains:
            return render_template('signup.html', message="Use Gmail, Yahoo, Outlook, phinmaed.com ")
        
        if password != confirm_password:
            return render_template('signup.html', message="Passwords do not match")
        
        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password):
            return render_template('signup.html', message="Password must be at least 8 characters, contain 1 digit, and 1 uppercase letter")
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return render_template('signup.html', message="Email already used, please log in")

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            return render_template('signup.html', message="Username already exists")

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username

            
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #  Hardcoded admin login
        if username == 'admin' and password == 'password':
            session['username'] = 'admin'
            session['role'] = 'admin'
            return redirect(url_for('admin_dashboard'))

        #  Check user from database
        user = User.query.filter_by(username=username).first()
        if not user:
            return render_template('login.html', message="Username not found. Please try again")
        elif not check_password_hash(user.password, password):
            return render_template('login.html', message="Incorrect password. Please try again")
        elif user.is_banned:
            return render_template('login.html', message="Your account has been banned.")
        else:
            session['username'] = user.username
            return redirect(url_for('dashboard'))

    return render_template('login.html')




def is_admin():
    return session.get('username') == 'admin'


@app.route('/admin/update', methods=['GET', 'POST'])
def admin_update():
    if not is_admin():
        return "Access Denied"

    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        new_update = Update(title=title, message=message)
        db.session.add(new_update)
        db.session.commit()
        return redirect(url_for('admin_update', message="Update has been posted"))

    updates = Update.query.order_by(Update.timestamp.desc()).all()
    message = request.args.get('message')  
    return render_template('admin_update.html', updates=updates, message=message)


@app.route('/admin/update/edit/<int:update_id>', methods=['GET', 'POST'])
def edit_update(update_id):
    if not is_admin():
        return "Access Denied"
    
    update = Update.query.get_or_404(update_id)

    if request.method == 'POST':
        update.title = request.form['title']
        update.message = request.form['message']
        db.session.commit()
        return redirect(url_for('admin_update', message="Changes saved"))

    return render_template('edit_update.html', update=update)


@app.route('/admin/update/delete/<int:update_id>', methods=['POST'])
def delete_update(update_id):
    if not is_admin():
        return jsonify({"message": "Access Denied", "success": False}), 403

    update = Update.query.get_or_404(update_id)
    db.session.delete(update)
    db.session.commit()

    return jsonify({"message": "Update has been deleted", "success": True})



@app.route('/admin/ban/<username>')
def ban_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user.is_banned = True
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/unban/<username>')
def unban_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user.is_banned = False
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete/<username>')
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        # Manually delete friendships first
        Friendship.query.filter((Friendship.user_id == user.id) | (Friendship.friend_id == user.id)).delete()
        Playlist.query.filter_by(user_id=user.id).delete()
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/media')
def admin_media():
    if session.get('username') != 'admin':
        return "Access Denied"

    playlists = Playlist.query.all()
    songs = Song.query.all()
    shared_items = Shared.query.all()

    return render_template("admin_media.html", playlists=playlists,
                           songs=songs,
                           shared_items=shared_items)



@app.route('/admin/delete_reported/<int:report_id>')
def delete_reported_content(report_id):
    report = Report.query.get(report_id)
    if report:
        if report.content_type == "song":
            song = Song.query.get(int(report.content))
            if song:
                db.session.delete(song)
        elif report.content_type == "playlist":
            playlist = Playlist.query.get(int(report.content))
            if playlist:
                db.session.delete(playlist)
        elif report.content_type == "user":
            user = User.query.filter_by(username=report.content).first()
            if user:
                db.session.delete(user)
        db.session.delete(report)
        db.session.commit()
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/dismiss_report/<int:report_id>')
def dismiss_report(report_id):
    report = Report.query.get(report_id)
    if report:
        db.session.delete(report)
        db.session.commit()
    return redirect(url_for('admin_dashboard'))


@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('username') != 'admin':
        return "Access Denied"

    # Total counts
    total_users = User.query.count()
    total_songs = Song.query.count()
    total_playlists = Playlist.query.count()

    # Recent signups (last 7 days)
    cutoff_date = datetime.utcnow() - timedelta(days=7)
    recent_signups = (
        db.session.query(db.func.date(User.created_at).label("date"), db.func.count(User.id).label("count"))
        .filter(User.created_at >= cutoff_date)
        .group_by(db.func.date(User.created_at))
        .all()
    )

    # Most active users (based on number of playlists)
    most_active_users = (
        db.session.query(User.username, db.func.count(Playlist.id).label("playlist_count"))
        .join(Playlist, User.id == Playlist.user_id)
        .group_by(User.id)
        .order_by(db.desc("playlist_count"))
        .limit(5)
        .all()
    )

    # Recent admin updates
    recent_admin_updates = Update.query.order_by(Update.timestamp.desc()).limit(5).all()

    # Shared content tracking
    shared_content = Shared.query.order_by(Shared.timestamp.desc()).all()

    # All users with playlist count and shared song count
    users = User.query.all()
    all_users = []
    for user in users:
        playlist_count = Playlist.query.filter_by(user_id=user.id).count()
        shared_count = Shared.query.filter_by(sender=user.username).count()
        all_users.append({
            "username": user.username,
            "email": user.email,
            "is_banned": user.is_banned,
            "playlist_count": playlist_count,
            "shared_song_count": shared_count
        })

    # Reports for moderation
    reports = Report.query.order_by(Report.timestamp.desc()).all()

    return render_template("admin_dashboard.html",
                           total_users=total_users,
                           total_songs=total_songs,
                           total_playlists=total_playlists,
                           recent_signups=recent_signups,
                           most_active_users=most_active_users,
                           recent_admin_updates=recent_admin_updates,
                           shared_content=shared_content,
                           all_users=all_users,
                           reports=reports)



@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    playlists = get_playlists(username)

    # Admin updates
    updates = Update.query.order_by(Update.timestamp.desc()).all()

    # Shared content received by the user
    shared_items = Shared.query.filter_by(receiver=username).order_by(Shared.timestamp.desc()).all()

    shared_songs = []
    shared_genres = []

    for item in shared_items:
        if item.content_type == 'song':
            song = Song.query.get(int(item.content))
            if song:
                shared_songs.append(song)
        elif item.content_type == 'genre':
            songs = Song.query.filter_by(genre=item.content).all()
            shared_genres.append({
                'genre': item.content,
                'songs': songs
            })

    # Recent songs (last 3 added)
    recent_songs = Song.query.order_by(Song.id.desc()).limit(3).all()

    # Random suggested songs
    suggested_songs = Song.query.order_by(db.func.random()).limit(3).all()

    return render_template(
        'dashboard.html',
        username=username,
        playlists=playlists,
        recent_songs=recent_songs,
        suggested_songs=suggested_songs,
        shared_songs=shared_songs,
        shared_genres=shared_genres,
        updates=updates
    )

@app.route('/share_song/<int:song_id>', methods=['GET'])
def share_song(song_id):
    friend_username = request.args.get('friend_username')
    song = Song.query.get(song_id)

    if not song:
        return "Song not found"

    song_data = {
        "title": song.title,
        "artist": song.artist,
        "file": song.file,
        "share_url": url_for('static', filename=song.file, _external=True)
    }

    if friend_username:
        shared = Shared(sender=session['username'], receiver=friend_username,
                        content_type='song', content=str(song_id))
        db.session.add(shared)
        db.session.commit()

    message = f"Song shared to {friend_username}" if friend_username else None
    return render_template('share_song.html', song=song_data, friend_username=friend_username, message=message)


@app.route('/share_genre/<username>/<genre>')
def share_genre(username, genre):
    friend_username = request.args.get('friend_username', None)
    genre_songs = Song.query.filter(Song.genre.ilike(genre)).all()

    if not genre_songs:
        return "No songs found for this genre."

    if friend_username:
        shared = Shared(sender=session['username'], receiver=friend_username,
                        content_type='genre', content=genre)
        db.session.add(shared)
        db.session.commit()
        message = f"Genre shared to {friend_username}"
    else:
        message = None

    return render_template('share_genre.html', username=username, genre=genre,
                           songs=genre_songs, friend_username=friend_username, message=message)

@app.route('/search_user', methods=['GET'])
def search_user():
    query = request.args.get('q')
    current_username = session.get('username')

    users = User.query.filter(
        User.username.ilike(f"%{query}%"),
        User.username != current_username,
        User.username != 'admin'
    ).all()

    results = [{"username": u.username} for u in users]
    return jsonify(results)



@app.route('/add_friend/<friend_username>', methods=['POST'])
def add_friend(friend_username):
    current_user = User.query.filter_by(username=session['username']).first()
    friend = User.query.filter_by(username=friend_username).first()

    if not friend:
        return jsonify({"success": False, "message": "User not found"})

    # Check if already friends
    existing = Friendship.query.filter_by(user_id=current_user.id, friend_id=friend.id).first()
    if existing:
        return jsonify({"success": False, "message": "Already friends"})

    new_friend = Friendship(user_id=current_user.id, friend_id=friend.id)
    db.session.add(new_friend)
    db.session.commit()
    return jsonify({"success": True, "message": "Friend added!"})


@app.route('/my_friends')
def my_friends():
    user = User.query.filter_by(username=session['username']).first()
    friendships = Friendship.query.filter_by(user_id=user.id).all()
    friend_usernames = [User.query.get(f.friend_id).username for f in friendships]
    return jsonify(friend_usernames)

@app.route('/create_group_playlist', methods=['POST'])
def create_group_playlist():
    playlist_name = request.form['playlist_name']
    friends_raw = request.form['friends']
    current_user = User.query.filter_by(username=session['username']).first()

    # Create playlist
    playlist = Playlist(name=playlist_name, user_id=current_user.id, is_group=True)
    db.session.add(playlist)
    db.session.commit()

    # Add members to group (including creator)
    usernames = [u.strip() for u in friends_raw.split(',') if u.strip()]
    usernames.append(current_user.username)

    for uname in set(usernames):
        user = User.query.filter_by(username=uname).first()
        if user:
            db.session.add(GroupMember(playlist_id=playlist.id, user_id=user.id))

    db.session.commit()
    return redirect('/dashboard')  # or render a success template

@app.route('/create_group_playlist', methods=['GET'])
def create_group_playlist_form():
    return render_template("group_playlist.html")


@app.route('/share_group_playlist', methods=['GET', 'POST'])
def share_group_playlist():
    user = User.query.filter_by(username=session['username']).first()
    message = ""

    if request.method == 'POST':
        playlist_name = request.form['playlist_name']
        friend_username = request.form['friend_username']

        playlist = Playlist.query.filter_by(name=playlist_name, user_id=user.id).first()
        friend = User.query.filter_by(username=friend_username).first()

        if not playlist or not friend:
            message = "Invalid playlist or friend"
        else:
            # Check if already shared
            exists = GroupMember.query.filter_by(playlist_id=playlist.id, user_id=friend.id).first()
            if not exists:
                db.session.add(GroupMember(playlist_id=playlist.id, user_id=friend.id))
                db.session.commit()
                message = "Playlist shared successfully!"
            else:
                message = "Playlist already shared with this user."

    # Show user’s group playlists
    playlists = [p.name for p in Playlist.query.filter_by(user_id=user.id, is_group=True).all()]
    return render_template("share_group_playlist.html", playlists=playlists, message=message)


@app.route('/ourteams')
def ourteam():
    return render_template('ourteams.html')
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/web/<username>', methods=['GET', 'POST'])
def web_interface(username):
    session['username'] = username
    user = User.query.filter_by(username=username).first()
    if not user:
        return redirect(url_for('login'))

    songs = Song.query.all()
    playlists = get_playlists(username)

    artist_name = request.args.get('artist_name')
    action = request.args.get('action')
    query = request.args.get('query')
    selected_genre = request.args.get('genre')
    playlist_name = request.args.get('playlist_name')
    song_id = request.args.get('song_id')
    playlist_target = request.args.get('playlist_target')

    # Log out
    if action == 'logout':
        session.clear()
        return redirect(url_for('login'))

    # Search
    elif action == 'search' and query:
        query_lower = query.lower()
        matched_songs = Song.query.filter(
            (Song.title.ilike(f'%{query_lower}%')) |
            (Song.artist.ilike(f'%{query_lower}%'))
        ).all()

        artist_match = Song.query.filter(Song.artist.ilike(query_lower)).all()
        is_artist_search = bool(artist_match and len(artist_match) == len(matched_songs))

        return render_template('dashboard.html', action='searchartist' if is_artist_search else 'search',
                               query=query, results=matched_songs, playlists=playlists,
                               is_artist_search=is_artist_search)

    # Share artist
    elif action == 'artist' and artist_name:
        artist_songs = Song.query.filter(Song.artist.ilike(artist_name)).all()
        friend_username = request.args.get('friend_username')
        message = f"Artist shared to {friend_username}" if friend_username else None
        share_url = url_for('web_interface', username=session['username'],
                            action='artistmusic', artist_name=artist_name, _external=True)
        return render_template('share_artist.html', username=username, artist_name=artist_name,
                               songs=artist_songs, share_url=share_url, message=message)

    # View all music
    elif action == 'allmusic':
        return render_template('dashboard.html', results=songs, playlists=playlists,
                               action='allmusic', playlist_target=playlist_target)

    # Filter by genre
    elif action == 'genre' and selected_genre:
        if selected_genre.lower() == 'all music':
            filtered_songs = songs
        else:
            filtered_songs = Song.query.filter(Song.genre.ilike(selected_genre)).all()
        return render_template('dashboard.html', genre=selected_genre,
                               results=filtered_songs, playlists=playlists)

    # Create playlist
    elif action == 'createplaylist' and playlist_name:
        existing = Playlist.query.filter_by(name=playlist_name, user_id=user.id).first()
        if existing:
            return render_template('dashboard.html', message="Playlist already exists.", playlists=playlists)
        new_pl = Playlist(name=playlist_name, user_id=user.id)
        db.session.add(new_pl)
        db.session.commit()
        playlists = get_playlists(username)
        return redirect(url_for('web_interface', username=username, action='allmusic', playlist_target=playlist_name))

    # Add song to playlist
    elif action == 'addtoplaylist' and song_id:
        target_playlist = Playlist.query.filter_by(name=playlist_target, user_id=user.id).first()
        if not target_playlist:
            return render_template('dashboard.html', message="Playlist not found.", playlists=playlists, results=songs)

        existing = PlaylistSong.query.filter_by(playlist_id=target_playlist.id, song_id=song_id).first()
        if existing:
            message = "Song already in playlist."
        else:
            new_entry = PlaylistSong(playlist_id=target_playlist.id, song_id=song_id)
            db.session.add(new_entry)
            db.session.commit()
            message = f"Added song to {playlist_target}."

        playlists = get_playlists(username)
        return render_template('dashboard.html', message=message, playlists=playlists, results=songs)

    # View playlist
    elif action == 'viewplaylist' and playlist_name:
        playlists = get_playlists(username)
        results = playlists.get(playlist_name, [])
        return render_template('dashboard.html', playlist_name=playlist_name,
                               results=results, playlists=playlists)

    # Delete playlist
    elif action == 'deleteplaylist' and playlist_name:
        target_playlist = Playlist.query.filter_by(name=playlist_name, user_id=user.id).first()
        if target_playlist:
            db.session.delete(target_playlist)
            db.session.commit()
            message = f"Playlist '{playlist_name}' deleted."
        else:
            message = "Playlist not found."
        playlists = get_playlists(username)
        return render_template('dashboard.html', message=message, playlists=playlists, results=songs)

    # Remove song from playlist
    elif action == 'remove_from_playlist' and playlist_name and song_id:
        target_playlist = Playlist.query.filter_by(name=playlist_name, user_id=user.id).first()
        if target_playlist:
            entry = PlaylistSong.query.filter_by(playlist_id=target_playlist.id, song_id=song_id).first()
            if entry:
                db.session.delete(entry)
                db.session.commit()
        playlists = get_playlists(username)
        results = playlists.get(playlist_name, [])
        return render_template('dashboard.html', playlist_name=playlist_name,
                               results=results, playlists=playlists)

    return render_template('dashboard.html', results=songs, playlists=playlists)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/check_user/<friend_username>')
def check_user(friend_username):
    exists = User.query.filter_by(username=friend_username).first() is not None
    return {"exists": exists}


@app.route('/share/<username>/<playlist_name>')
def share_playlist(username, playlist_name):
    playlists = get_playlists(username)
    playlist = playlists.get(playlist_name, [])
    return render_template('share.html', username=username, playlist_name=playlist_name, songs=playlist)

if __name__ == '__main__':
    app.run(debug=True)

