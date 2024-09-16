from flask import Flask, render_template, request, redirect, url_for,flash
from model import  User, Album, Song, Playlist
from flask_login import LoginManager,login_user,current_user,logout_user
from datetime import datetime
from sqlalchemy import or_
from extension import db
from graph import *
from resources import api



app = Flask(__name__)
app.config['SECRET_KEY'] = 'spotify123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musicdb.sqlite'
db.init_app(app)
api.init_app(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id): 
    return User.query.get(user_id)




#----------------------------------homepage-----------------------------------------------
@app.route('/')
def home():
    return render_template("index.html")


#------------------------------------------------User register------------------------------------------------
@app.route('/register' ,methods=['GET','POST'])
def register():
    userr=User.query.all()
    if request.method == 'GET':
        return render_template("register_user.html")
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        creator=request.form.get('creator')
        for a in userr:
            if a.email==email:
                flash('An account with this mail is already registered.', "danger")
                return render_template('register_user.html')
            elif a.name==username:
                flash('Username is already taken please choose another username',"danger")
                return render_template('register_user.html')
        user =User(name=username,email=email, password=password , creator=creator)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_login'))
    return render_template('register_user.html')


#----------------------------User login-------------------------------------------------------
@app.route('/user_login', methods=['GET','POST'])
def user_login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        User(name=name, password=password)
        user=db.session.query(User).filter(User.name==name, User.password==password ).first()

        if user and user.password == password:
            flash("valid username and password", 'success') 
            login_user(user)
            return redirect(url_for('user_dashboard'))  

        elif user==None:
            flash("Username does not exist, please create your account.", "danger")

        else:
            flash("Wrong password, please try again!","danger")

    
    return render_template('user_login.html')


#-----------------------------User dashboard-------------------------------------------------
@app.route("/user_dashboard", methods=["GET","POST"])
def user_dashboard():
    album=Album.query.all()
    song=Song.query.all()
    user=current_user
    return render_template('user_dashboard.html', album=album,user=user, song=song)


#---------------------------admin dashboard---------------------------------------------------
@app.route("/admin_dashboard", methods=["GET","POST"])
def admin_dashboard():
            total_users_count = User.query.count()
            total_creators_count = User.query.filter_by(creator="yes").count()
            total_songs_count = Song.query.count()
            total_albums_count = Album.query.count()
            blacklisted_creators_count = User.query.filter_by(blacklist=True).count()
            flagged_songs_count = Song.query.filter_by(flag=True).count()
            return render_template('admin_dashboard.html',
                           total_users_count=total_users_count,
                           total_creators_count=total_creators_count,
                           total_songs_count=total_songs_count,
                           total_albums_count=total_albums_count,
                           blacklisted_creators_count=blacklisted_creators_count,
                           flagged_songs_count=flagged_songs_count)
    


#----------------------------admin login---------------------------------------------------------
@app.route("/admin_login", methods=["GET","POST"])
def admin_login():
    if request.method=="POST":
        admin={"name": "admin1", "e-mail": "admin1@gmail.com", "password": "a1d2m3i4n5"}
        name=request.form.get('name')
        password=request.form.get('password')
        if admin["name"]==name and admin["password"]==password :
            pie_chart()
            bar_graph()
            total_users_count = User.query.count()
            total_creators_count = User.query.filter_by(creator="yes").count()
            total_songs_count = Song.query.count()
            total_albums_count = Album.query.count()
            blacklisted_creators_count = User.query.filter_by(blacklist=True).count()
            flagged_songs_count = Song.query.filter_by(flag=True).count()
            return render_template('admin_dashboard.html',
                           total_users_count=total_users_count,
                           total_creators_count=total_creators_count,
                           total_songs_count=total_songs_count,
                           total_albums_count=total_albums_count,
                           blacklisted_creators_count=blacklisted_creators_count,
                           flagged_songs_count=flagged_songs_count)
        else:
            flash("incorrent credentials, please try again!", "danger")
            return render_template('admin_login.html')
    if request.method=="GET":
        return render_template('admin_login.html')

#---------------------------------creator registration----------------------------------------------
@app.route('/register_creator')
def register_creator():
    user = User.query.filter_by(id=current_user.id).first()
    if user.creator!="yes":
        user.creator="yes"
        db.session.commit()
        flash("Successfully registered as creator", "success")
    else:
        flash("already registered as creator!","success")
    return redirect(url_for('creator_dashboard'))

#--------------------------------play a song--------------------------------------------------------
@app.route('/play_song/<int:id>')
def play_song(id):
    song=Song.query.all()
    c=Song.query.get(id)
    user=current_user
    return render_template('play_song.html',song=song,c=c,user=user)


#---------------------------------upload songs--------------------------------------------------------
@app.route('/upload_songs/<int:id>', methods=["GET","POST"])
def upload_songs(id):
    album=Album.query.all()
    user=current_user
    if request.method=="GET":
        if user.blacklist==True:
            flash("You have been blacklisted, please revise your uploaded content if you want to upload more content.","danger")
            return redirect(url_for("creator_dashboard" , user_id=user.id))
        return render_template('upload_songs.html',user=user, album=album)
    if request.method=="POST":
        a_id=request.form.get('album')
        s_name=request.form.get('name')
        lyrics=request.form.get('lyrics')
        genre=request.form.get('genre')
        c_name=request.form.get('creator_name')
        c_date=datetime.strptime(request.form['creation_date'], '%Y-%m-%d')
        user_id=user.id
   
        s=Song(name=s_name,lyrics=lyrics, creator_name=c_name, creation_date=c_date, genre=genre, album_id=a_id, user_id=user_id)
        db.session.add(s)
        db.session.commit()
        flash("Song has been uploaded.", "success")
        return redirect(url_for('creator_dashboard'))



#-------------------------------------edit song--------------------------------------------------------
@app.route("/edit_song/<int:userr>/<int:id>" , methods = ["GET","POST"])
def edit_song(id,userr):
    c= Song.query.get(id)
    userr=current_user
    album=Album.query.all()
    if request.method=='GET':
        return render_template("edit_song.html" , c=c, userr=userr, album=album)
    if request.method=='POST':
        c.name=request.form["song_name"]
        c.lyrics=request.form["lyrics"]
        c.genre=request.form["genre"]
        c.creator_name=request.form["creator_name"]
        c.album_id=request.form["album"]
        db.session.commit()
        flash('Song has been edited', "success")
        return redirect('/creator_dashboard')
    
#-------------------------------------edit album---------------------------------------------------
@app.route("/edit_album/<int:id>" , methods = ["GET","POST"])
def edit_album(id):
    c= Album.query.get(id)
    user=current_user
    if request.method=='GET':
        return render_template("edit_album.html" , c=c, user=user)
    if request.method=='POST':
        c.name=request.form["name"]
        db.session.commit()
        flash('Album name has been edited', "success")
        return redirect(url_for('creator_dashboard'))


#-------------------------------------edit playlist----------------------------------------------------
@app.route('/edit_playlist/<int:user_id>/<int:playlist_id>',methods=["GET", "POST"])
def edit_playlist(user_id,playlist_id):
    if request.method=="GET":

        user=current_user
        p = Playlist.query.get(playlist_id)
        song = Song.query.all()
        return render_template("edit_playlist.html", user=user, p=p, song=song)
    
    if request.method=="POST":
        user=current_user
        song_id = request.form.get("song_id")
        playlist = Playlist.query.get(playlist_id)
        song = Song.query.get(song_id)

    
        if song not in playlist.songs:
            playlist.songs.append(song)
            db.session.commit()

            flash("Song has been added to the playlist.","success")
            return redirect(url_for('display_playlist', user_id=user_id, playlist_id=playlist_id))
        else:
            flash("Song is already in the playlist", "danger")
            return redirect(url_for('display_playlist', user_id=user_id, playlist_id=playlist_id))


#-------------------------------------------delete song from playlist----------------------------------
@app.route('/delete_playlist_song/<int:user_id>/<int:playlist_id>/<int:song_id>')
def delete_playlist_song(playlist_id,song_id,user_id):
        playlist = Playlist.query.get(playlist_id)
        song = Song.query.get(song_id)
        playlist.songs.remove(song)
        db.session.commit()
        flash('Song removed from playlist successfully.', 'success')
        return redirect(url_for('display_playlist', user_id=user_id, playlist_id=playlist_id))

#-------------------------------------display_playlist------------------------------------------------
@app.route('/display_playlist/<int:user_id>', methods=["GET", "POST"])
def display_playlist(user_id):
    if request.method == "GET":
        user = current_user
        songs = Song.query.all()
        playlist=Playlist.query.all()
        return render_template("display_playlist.html", songs=songs, user=user, playlist=playlist)

    if request.method == "POST":
        name = request.form['playlist_name']
        p = Playlist(name=name, user_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        flash("Playlist added successfully!","success")

        
        return redirect(url_for("display_playlist", user_id=current_user.id))
    
#-----------------------------------------edit playlist name-------------------------------------------
@app.route('/editt_playlist/<int:user_id>/<int:playlist_id>', methods=["GET","POST"])
def editt_playlist(user_id,playlist_id):
    playlist=Playlist.query.get(playlist_id)
    playlists=Playlist.query.all()
    if request.method=="GET":
        return render_template('editt_playlist.html',user_id=user_id,playlist_id=playlist_id, playlists=playlists)
    
    if request.method=="POST":
        songs=Song.query.all()
        name=request.form['name']
        playlist.name=name
        db.session.commit()
        flash("playlist name changesd successfully", 'success')
        return redirect(url_for("display_playlist",user_id=user_id))

#--------------------------------------delete playlist-------------------------------------------------
from flask import redirect, flash

@app.route('/delete_playlist/<int:id>', methods=["POST", "GET"])
def delete_playlist(id):
    user = current_user
    if request.method == "GET":
        playlist = Playlist.query.get(id)
        if playlist:
            db.session.delete(playlist)
            db.session.commit()
            flash("Playlist has been deleted successfully.", "success")
        else:
            flash("Playlist not found.", "danger")
        
        return redirect(url_for('display_playlist',user_id=user.id))


    
#---------------------------------------creator_dashboard----------------------------------------------
@app.route('/creator_dashboard')
def creator_dashboard():
    user=current_user
    song=Song.query.all()
    album=Album.query.all()
    songs=Song.query.filter_by(user_id=user.id).all()
    albums=Album.query.filter_by(user_id=user.id).all()
    return render_template("creator_dashboard.html", user=user,song=song, album=album, albums=albums, songs=songs)


#----------------------------------------create_album--------------------------------------------------

@app.route('/create_album/<int:user_id>', methods=["GET", "POST"])
def create_album(user_id):
    if request.method == "GET":
        user = current_user
        songs = Song.query.all()
        if user.blacklist==False:
            return render_template("create_album.html", songs=songs, user=user)
        else:
            flash("You have been blacklisted, please revise your uploaded content if you want to upload more content.",'danger')
            return redirect(url_for("creator_dashboard" , user_id=user.id))

    if request.method == "POST":
        user = current_user
        album_name = request.form.get("name")
        
    
        existing_album = Album.query.filter_by(name=album_name).first()

        if existing_album is None:

            new_album = Album(name=album_name, user_id=user.id)
            db.session.add(new_album)
            db.session.commit()

            flash("Album has been added.",'success')
            return redirect(url_for('creator_dashboard', user_id=user.id))
        else:

            flash("Album name already exists, please add a different name.","danger")
            return redirect(url_for('create_album', user_id=user.id))

    return render_template("create_album.html", user=user)




#------------------------------------------admin_songs--------------------------------------------------
@app.route('/admin_songs', methods=["GET","POST"])
def admin_songs():
    if request.method=="GET":
        songs=Song.query.all()
        return render_template("admin_songs.html", songs=songs)
    
#-------------------------------------------flag songs-------------------------------------------------
@app.route('/admin_songs/<int:song_id>', methods=["POST"])
def admin_songss(song_id):
        flagg=request.form['flag_action']
        if request.method=="POST":
            flag_song=Song.query.get(song_id)
            if flagg=='1':
                flag_song.flag=True
                flash("Song has been flagged","success")
                db.session.commit()
            else:
                flag_song.flag=False
                flash("song has been unflagged","success")
                db.session.commit()
            
        return redirect(url_for('admin_songs'))

#------------------------------------------flag albums--------------------------------------------------
@app.route('/admin_albums/<int:album_id>', methods=["POST"])
def admin_albumss(album_id):
        flagg=request.form['flag_action']
        if request.method=="POST":
            flag_album=Album.query.get(album_id)
            if flagg=='1':
                flag_album.flag=True
                flash("Album has been flagged","success")
                db.session.commit()
            else:
                flag_album.flag=False
                flash("Album has been unflagged","success")
                db.session.commit()
            
        return redirect(url_for('admin_albums'))


#------------------------------------------admin_creators------------------------------------------------
@app.route('/admin_creators')
def admin_creators():
    users=User.query.all()
    return render_template("admin_creators.html", users=users)



#------------------------------------------blacklist creator--------------------------------------------

@app.route('/blacklist_creator/<int:user_id>', methods=["POST"])
def blacklist_creator(user_id):
    if request.method=="POST":
        black=User.query.get(user_id)
        form=request.form['blacklist_action']
        if form=="1":
            black.blacklist=True
            db.session.commit()
            flash("User has been blacklisted successfully.","success")
            
        else:
            black.blacklist=False
            db.session.commit()
            flash("User has been whitelisted successfully.","success")

        return redirect(url_for('admin_creators'))

#------------------------------------------admin_albums---------------------------------------------------
@app.route('/admin_albums', methods=["GET", "POST"])
def admin_albums():
    if request.method=="GET":
        albums=Album.query.all()
        return render_template("admin_albums.html" ,albums=albums)

    

#-----------------------------------------album song-------------------------------------------------------
@app.route('/album_song/<int:id>')
def album_song(id):
    a=Album.query.filter_by(id=id).first()
    songs=Song.query.filter_by(album_id=a.id).all()
    user=current_user
    return render_template("album_song.html",a=a,user=user,songs=songs)

#--------------------------------------------display_creator----------------------------------------------
@app.route('/display_creator/<int:id>')
def display_creator(id):
    a=Album.query.filter_by(id=id).first()
    album=Album.query.all()
    song=Song.query.all()
    user=current_user
    return render_template("display_creator.html",album=album,song=song,a=a,user=user)

#---------------------------------------------delete song-------------------------------------------------

@app.route('/delete_song/<int:song_id>', methods=["GET"])
def delete_song(song_id):
        user=current_user
        a=Album.query.filter_by(user_id=user.id).first()
        song=Song.query.all()
        if request.method=="GET":
            song = Song.query.filter_by(id=song_id).first()
            db.session.delete(song)
            db.session.commit()
            flash("Song Deleted Successfully","success")
            return redirect('/creator_dashboard')    

#---------------------------------------admin delete song-------------------------------------------------
@app.route('/admin_delete_song/<int:song_id>')
def admin_delete_song(song_id):
    songs=Song.query.get(song_id)
    db.session.delete(songs)
    db.session.commit()
    flash("song has been deleted successfully.","success")
    return redirect("/admin_songs")

#----------------------------------------admin delete album-----------------------------------------------

@app.route('/admin_delete_album/<int:album_id>')
def admin_delete_album(album_id):
        album=  Album.query.get(album_id)
        db.session.delete(album)
        db.session.commit()
        flash("Album has been deleted successfully.","success")
        return redirect("/admin_albums")
    

#--------------------------------------delete album-----------------------------------------------------------
        
@app.route('/delete_album/<int:album_id>', methods=["GET"])
def delete_album(album_id):
        album=Album.query.get(album_id)
        if request.method=="GET":
            db.session.delete(album)
            db.session.commit()
            flash(" Album Deleted Successfully","success")
            return redirect('/creator_dashboard')       


#----------------------------------------logout-------------------------------------------------------------
@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out successfully!","success")
    return redirect(url_for('home'))

#-----------------------------------------rate song---------------------------------------------------------
@app.route('/rate_song/<int:id>',  methods=['GET','POST'])
def rate_song(id):
    if request.method=="POST":
        r=float(request.form['rating'])
        a=Song.query.get(id)
        n=a.number
        rate=a.rating
        if n==0 or n==None:
            if n==None:
                n=0
            a.rating=r
            n+=1
            a.number=n
            db.session.commit()
        else:
            rate=round(((rate*n)+r)/(n+1),1)
            n+=1
            a.rating=rate
            a.number=n
            db.session.commit()
        return(redirect(url_for('user_dashboard')))

#-------------------------------------------search------------------------------------------------------
@app.route("/search" , methods=["GET" , "POST"])
def search():
    if request.method=="GET":
        return render_template("search.html")
    if request.method=="POST":
        query = request.form['query']
        query = f"%{query}%"
    
        results = Song.query.filter( or_(
                        Song.name.contains(query),
                        Song.creator_name.contains(query),
                        Song.genre.contains(query)
                    )).all()
        resultss = Album.query.filter( or_(
                        Album.name.contains(query))).all()
        album=Album.query.all()
        song=Song.query.all()
        user=current_user
        return render_template('search.html', album=album,user=user, song=song, results=results, resultss=resultss)
