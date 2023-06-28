from flask import Flask, redirect, request
from google_auth_oauthlib.flow import Flow


URL_USERINFO = 'https://www.googleapis.com/userinfo/v2/me'


app = Flask("Google Login App")
app.secret_key = "YourSecretKeyHere"  # Secret key is needed for OAuth 2.0


cache = {}
flow = Flow.from_client_secrets_file(
    client_secrets_file='./client_secrets.json',
    scopes=["https://www.googleapis.com/auth/userinfo.email", "openid", "https://www.googleapis.com/auth/userinfo.profile"],
    redirect_uri='https://127.0.0.1:5000/login/callback',
)


@app.route("/")
def index():
    if 'name' in cache:
        return f"Hello {cache['name']}! <a href='/logout'>Logout</a>"
    return "<a href='/login'>Login</a>"


@app.route('/login')
def login():
    return redirect(flow.authorization_url()[0])


@app.route('/login/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)
    google = flow.authorized_session()
    user = google.get(URL_USERINFO).json()
    cache.update(user)
    return redirect('/')


@app.route('/logout')
def logout():
    cache.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run(ssl_context='adhoc', debug=True)