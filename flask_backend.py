from flask import Flask, render_template, request
from parser import start
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_process', methods=['POST'])
def start_process():
    if request.method == 'POST':
        result = start()
        return result


@app.route('/db')
def db():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM games')
    games = cursor.fetchall()
    connection.close()
    return render_template('db.html', games=games)


@app.route('/filter', methods=['POST'])
def filter_games():
    min_price = request.form.get('min_price')
    max_price = request.form.get('max_price')
    free_games = request.form.get('free_games')

    def convert_price(price):
        if price.lower() == 'free':
            return 0
        else:
            return int(price.split()[0])

    min_price = convert_price(min_price) if min_price else 0
    max_price = convert_price(max_price) if max_price else float('inf')

    connection = connect_db()
    cursor = connection.cursor()

    if free_games:
        cursor.execute('SELECT * FROM games WHERE price = "Free"')
    else:
        if min_price and max_price:
            cursor.execute('SELECT * FROM games WHERE CONVERT(price, INTEGER) BETWEEN ? AND ? AND price != "Free"',
                           (min_price, max_price))
        elif min_price:
            cursor.execute('SELECT * FROM games WHERE CONVERT(price, INTEGER) >= ? AND price != "Free"',
                           (min_price,))
        elif max_price:
            cursor.execute('SELECT * FROM games WHERE CONVERT(price, INTEGER) <= ? AND price != "Free"',
                           (max_price,))
        else:
            cursor.execute('SELECT * FROM games WHERE price != "Free"')

    games = cursor.fetchall()
    connection.close()
    return render_template('filtered_games.html', games=games)


def connect_db():
    return sqlite3.connect('games.db')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
