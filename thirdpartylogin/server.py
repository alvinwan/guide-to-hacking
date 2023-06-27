from flask import Flask, session
from flask_google_login import FlaskGoogleLogin


app = Flask("Google Login App")
app.secret_key = "YourSecretKeyHere"  # Secret key is needed for OAuth 2.0
FlaskGoogleLogin(app)


@app.route("/")
def index():
    if 'google_id' in session:
        return f"Hello {session['name']}! <a href='/logout'>Logout</a>"
    return "<a href='/login'>Login</a>"


if __name__ == "__main__":
    app.run(ssl_context='adhoc', debug=True)