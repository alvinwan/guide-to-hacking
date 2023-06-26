from flask import Flask, session
from flask_google_login import FlaskGoogleLogin
import webview


app = Flask("Google Login App")
app.secret_key = "YourSecretKeyHere"  # Secret key is needed for OAuth 2.0
login = FlaskGoogleLogin(app)


@app.route("/")
def index():
    if 'google_id' in session:
        return f"Hello {session['name']}! <a href='/logout'>Logout</a>"
    return "<a href='/login'>Login</a>"


if __name__ == '__main__':
    keyfile, certfile = webview.generate_ssl_cert()
    ssl = {'keyfile': keyfile, 'certfile': certfile}
    webview.create_window('Flask example', app, http_port=5000, server_args=ssl)
    webview.start()