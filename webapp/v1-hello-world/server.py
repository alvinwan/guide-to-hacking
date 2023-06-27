from flask import Flask

app = Flask(__name__)  # init web app

@app.route("/")  # define webpage with / URL
def hello_world():  # function run when user accesses /
    return "<p>Hello, World!</p>"  # return simple HTML webpage

if __name__ == '__main__':
    app.run(debug=True)  # start the web app