from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "challenges.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
@app.route("/challenges")
def list_challenges():
    conn = get_db()
    challenges = conn.execute(
        "SELECT * FROM challenges ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return render_template("challenges.html", challenges=challenges)


@app.route("/add", methods=["GET", "POST"])
def add_challenge():
    if request.method == "POST":
        challenger = request.form["challenger"]
        opponent = request.form["opponent"]
        game_choice = request.form["game"]
        custom_game = request.form.get("custom_game")

        game = custom_game if game_choice == "OTHER" else game_choice

        conn = get_db()
        conn.execute(
            """
            INSERT INTO challenges
            (challenger, opponent, game, status, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (challenger, opponent, game, "PENDING", datetime.now()),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("list_challenges"))

    return render_template("new_challenge.html")


@app.route("/challenge/<int:challenge_id>")
def challenge_detail(challenge_id):
    conn = get_db()
    challenge = conn.execute(
        "SELECT * FROM challenges WHERE id = ?", (challenge_id,)
    ).fetchone()
    conn.close()
    return render_template("challenge_detail.html", challenge=challenge)


@app.route("/challenge/<int:challenge_id>/accept", methods=["POST"])
def accept_challenge(challenge_id):
    conn = get_db()
    conn.execute(
        "UPDATE challenges SET status = 'ACCEPTED' WHERE id = ?",
        (challenge_id,)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("challenge_detail", challenge_id=challenge_id))


@app.route("/challenge/<int:challenge_id>/complete", methods=["POST"])
def complete_challenge(challenge_id):
    winner = request.form["winner"]

    conn = get_db()
    conn.execute(
        """
        UPDATE challenges
        SET status = 'COMPLETED', winner = ?
        WHERE id = ?
        """,
        (winner, challenge_id),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("challenge_detail", challenge_id=challenge_id))


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            challenger TEXT NOT NULL,
            opponent TEXT NOT NULL,
            game TEXT NOT NULL,
            status TEXT NOT NULL,
            winner TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
