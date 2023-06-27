from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_world():
    conn = sqlite3.connect('todos.db')  # connect to our database stored in todos.db
    todos = conn.execute('SELECT * FROM todos').fetchall()  # grab all rows from our todos table
    return render_template('index.html', todos=todos)  # render our template with the todos we grabbed

if __name__ == '__main__':
    app.run(debug=True)