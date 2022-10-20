from flask import Flask, request, render_template, redirect, g
import sqlite3
import os
app = Flask('')

PATH = os.path.abspath(__file__ + '/..')
DATABASE = os.path.join(PATH, 'db.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        cur = db.cursor()
        create_table = ''' CREATE TABLE films(
            movie title VARCHAR(255),
            director VARCHAR(255),
            film genre VARCHAR(255),
            duration int,
            graduation_year int
        )'''
        # cur.execute(create_table)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET','POST'])
def index():
    db = get_db()
    cur = db.cursor()
    delete_value = ''' DELETE FROM films WHERE director = "Джеймс Кемерон"'''
    cur.execute(delete_value)
    if request.method == 'POST':
        movie_title = request.form.get('movie title')
        director = request.form.get('director')
        film_genre = request.form.get('film genre')
        duration = request.form.get('duration')
        graduation_year = request.form.get('graduation_year') 
        new_film = f''' INSERT INTO films (movie, director, film, duration, graduation_year) 
                VALUES ("{movie_title}", "{director}", "{film_genre}", {duration}, {graduation_year});'''
        cur.execute(new_film)
        db.commit()
    select_db = '''SELECT movie title FROM films;'''
    cur.execute(select_db)
    films = cur.fetchall()
    for i in range(len(films)):
        films[i] = films[i][0]
    db.commit()
    return render_template('base.html', films = films)

app.run(debug=True)