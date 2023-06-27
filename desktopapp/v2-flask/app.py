from flask import Flask
import webview

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    webview.create_window('Flask example', app)
    webview.start()