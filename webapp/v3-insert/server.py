from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])  # accepted both GET (normal) and POST (form submission) requests
def hello_world():
    conn = sqlite3.connect('todos.db')
    if request.method == 'POST':  # if form submission
        conn.execute('INSERT INTO todos (text) VALUES (?)', (request.form['text'],))  # define a command that creates a new todo, where the text comes from the input field named 'text'
        conn.commit()  # run the command
    todos = conn.execute('SELECT * FROM todos').fetchall()
    return render_template('index.html', todos=todos)

if __name__ == '__main__':
    app.run(debug=True)