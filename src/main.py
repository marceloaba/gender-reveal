from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def init_db():
    with sqlite3.connect("./data/gender_reveal.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS guests (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            message TEXT
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS votes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            woman1 TEXT CHECK(woman1 IN ('Boy', 'Girl')),
                            woman2 TEXT CHECK(woman2 IN ('Boy', 'Girl'))
                          )''')
        conn.commit()


def get_vote_counts():
    with sqlite3.connect("./data/gender_reveal.db") as conn:
        cursor = conn.cursor()

        # Counting votes for Woman 1 (Nathalia & Marcelo)
        cursor.execute("SELECT COUNT(*) FROM votes WHERE woman1='Boy'")
        woman1_boy = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM votes WHERE woman1='Girl'")
        woman1_girl = cursor.fetchone()[0]

        # Counting votes for Woman 2 (Greyce & Winter)
        cursor.execute("SELECT COUNT(*) FROM votes WHERE woman2='Boy'")
        woman2_boy = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM votes WHERE woman2='Girl'")
        woman2_girl = cursor.fetchone()[0]

    return {
        'woman1_boy': woman1_boy,
        'woman1_girl': woman1_girl,
        'woman2_boy': woman2_boy,
        'woman2_girl': woman2_girl
    }


def get_guests_and_votes():
    with sqlite3.connect("./data/gender_reveal.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT guests.name, guests.message, votes.woman1, votes.woman2
                          FROM guests
                          LEFT JOIN votes ON guests.id = votes.id''')
        guests = cursor.fetchall()

    return guests


@app.route('/', methods=['GET', 'POST'])
def home():
    vote_counts = get_vote_counts()

    if request.method == 'POST':
        name = request.form['name']
        message = request.form.get('message', '')
        woman1_vote = request.form.get('woman1')
        woman2_vote = request.form.get('woman2')

        with sqlite3.connect("./data/gender_reveal.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO guests (name, message) VALUES (?, ?)", (name, message))
            if woman1_vote or woman2_vote:
                cursor.execute("INSERT INTO votes (woman1, woman2) VALUES (?, ?)", (woman1_vote, woman2_vote))
            conn.commit()

        flash('Thank you! Your vote has been recorded.')
        return redirect(url_for('home'))

    return render_template('index.html', vote_counts=vote_counts)


@app.route('/vote_results')
def vote_results():
    guests_and_votes = get_guests_and_votes()
    vote_counts = get_vote_counts()

    return render_template('vote.html', guests_and_votes=guests_and_votes, vote_counts=vote_counts)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_PORT"))
