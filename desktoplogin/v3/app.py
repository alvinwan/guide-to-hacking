from flask import Flask, session
from simple_flask_google_login import SimpleFlaskGoogleLogin
import webview
import webbrowser


def url_handler(url):
    webbrowser.open(url)
    return f"If you aren't redirected automatically, click <a href='{url}' target='_blank'>here</>"


app = Flask("Google Login App")
app.secret_key = "YourSecretKeyHere"  # Secret key is needed for OAuth 2.0
login = SimpleFlaskGoogleLogin(
    app, authorization_url_handler=url_handler,
    redirect_uri='https://desktop-login.glitch.me'
)


@app.route("/")
def index():
    if 'name' in session:
        return f"Hello {session['name']}! <a href='/logout'>Logout</a>"
    import sys
    return f"<html style='background-color:gray'><a href='/login'>Login</a> {sys.argv}</html>"


if __name__ == '__main__':
    webview.create_window('Flask example', app)
    webview.start()