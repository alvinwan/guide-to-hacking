from flask import Flask, session
from simple_flask_google_login import SimpleFlaskGoogleLogin


app = Flask("Google Login App")
app.secret_key = "YourSecretKeyHere"  # Secret key is needed for OAuth 2.0
SimpleFlaskGoogleLogin(app)


@app.route("/")
def index():
    if 'name' in session:
        return f"Hello {session['name']}! <a href='/logout'>Logout</a>"
    return "<a href='/login'>Login</a>"


if __name__ == "__main__":
    app.run(ssl_context='adhoc', debug=True)