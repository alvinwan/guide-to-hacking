from flask import Flask, session, url_for
from simple_flask_google_login import SimpleFlaskGoogleLogin
import webview
import webbrowser
import sys
from qtpy.QtWidgets import QApplication
from qtpy.QtCore import QEvent
import webview.platforms.qt


class MyApp(QApplication):
    def event(self, event: QEvent):
        if event.type() == QEvent.Type.FileOpen:
            url = event.url()
            if 'code=' in url.query():
                window.load_url(f"/login/callback?{url.query()}")
        return super(QApplication, self).event(event)


def url_handler(url):
    webbrowser.open(url)
    return f"If you aren't redirected automatically, click <a href='{url}' target='_blank'>here</a>"


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
    return f"<a href='/login'>Login</a>"


if __name__ == '__main__':
    application = MyApp(sys.argv)
    window = webview.create_window('Flask example', app)
    webview.start(gui='qt')