from flask import Flask, session, url_for
from simple_flask_google_login import SimpleFlaskGoogleLogin
import webview
import webbrowser
import webview.platforms.qt
from qtpy.QtWidgets import QApplication
from qtpy.QtCore import QEvent
from urllib.parse import urlparse, parse_qs


def event_handler(self, event: QEvent): # override the event method
    if event.type() == QEvent.Type.FileOpen: # filter the File Open event
        url = event.url()
        url = urlparse(url.toString())
        params = parse_qs(url.query)
        if 'code' in params:
            code = params['code'][0]
            state = params['state'][0]
            window.load_url(f"/login/callback?code={code}&state={state}")
    return super(QApplication, self).event(event)
webview.platforms.qt.QApplication.event = event_handler


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
    window = webview.create_window('Flask example', app)
    webview.start(gui='qt')