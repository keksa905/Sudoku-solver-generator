import os   
from flask import Flask, render_template, request, redirect, url_for, flash
import numpy as np
from core.sudoku import Sudoku
import constants.const as const
import core.generator as gen
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
DEBUG = (os.getenv("DEBUG") == 'true' or os.getenv("DEBUG") == 'True')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = os.getenv('PORT', '5000')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    return render_template("home.html")


@app.route("/hello/<name>")
def hello(name):
    html = f"<body> <h1> Hello {name}! </h1> \n <a href='/'> return back </a> </body>"
    return html


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/solver")
def sudoku():
    return render_template("sudoku.html")


# default sudoku for game
play_sudoku = Sudoku(const.DEFAULT_SUDOKU)
play_sudoku.solve()


@app.route("/play", methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        data = request.form
        data = prepare_sudoku_data(data)
        s = Sudoku(data)
        if s.solve():
            comparison = s.data == s.state
            if comparison.all():
                flash("Congratulations! You solved it successfully!", "success")
            else:
                flash("Your progress is correct!", "success")
        else:
            flash("Your progress is incorrect", "warning")

        return render_template("to_solve.html", sudoku=play_sudoku.data, current_sudoku=s.data)

    return render_template("to_solve.html", sudoku=play_sudoku.data)


@app.route("/generate_sudoku", methods=["POST"])
def generate_sudoku():
    global play_sudoku
    if "generate_easy" in request.form:
        play_sudoku = gen.generate(9, 3, 36)
    elif "generate_medium" in request.form:
        play_sudoku = gen.generate(9, 3, 31)
    elif "generate_hard" in request.form:
        play_sudoku = gen.generate(9, 3, 26)
    else:
        print("default")
        play_sudoku = gen.generate(9, 3, 35)

    play_sudoku.solve()

    return redirect(url_for("play"))


@app.route('/solution', methods=['POST'])
def solution():
    data = request.form
    data = prepare_sudoku_data(data)
    s = Sudoku(data)
    if s.solve():
        return render_template("solution.html", solved_puzzle=s.state)
    else:
        flash("Not solvable Sudoku", "danger")
        return render_template("sudoku.html")


def prepare_sudoku_data(data) -> np.ndarray:
    """
    Converts input from request.form to a numpy 2D array of integers for init of Sudoku.
    """
    rows = []
    row = []
    for i, val in enumerate(data.values()):
        if val == '' or val == '.':
            row.append(0)
        elif int(val) in range(1, 10):
            row.append(int(val))

        if i % 9 == 8:
            rows.append(row)
            row = []

    output = np.array(rows, int)
    return output


def main():
    app.run(debug=DEBUG, host=HOST, port=PORT)


if __name__ == "__main__":
    main()
