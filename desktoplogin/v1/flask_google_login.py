import os
import pathlib
from flask import session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests


class FlaskGoogleLogin:
    """
    This class will force HTTPs on all requests
    """
    def __init__(
        self,
        app=None,
        client_secrets_path="./client_secrets.json",
        scopes=["https://www.googleapis.com/auth/userinfo.email", "openid", "https://www.googleapis.com/auth/userinfo.profile"],
        login_endpoint="/login",
        login_redirect="/",
        callback_endpoint="/login/callback",
        logout_endpoint="/logout",
        logout_redirect="/",
    ):
        self.login_endpoint = login_endpoint
        self.login_redirect = login_redirect
        self.callback_endpoint = callback_endpoint
        self.logout_endpoint = logout_endpoint
        self.logout_redirect = logout_redirect
        self.scopes = scopes
        self.client_secrets_path = client_secrets_path
        self._flow = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.app.add_url_rule(self.login_endpoint, view_func=self.login_page)
        self.app.add_url_rule(self.callback_endpoint, view_func=self.callback_page)
        self.app.add_url_rule(self.logout_endpoint, view_func=self.logout_page)
        self.app.before_request(self.before_request)

    @property
    def flow(self):
        """Must be called from within a route"""
        if self._flow is None:
            path = self.client_secrets_path
            if path.startswith('.'):
                path = os.path.join(pathlib.Path(__file__).parent, path)
            self._flow = Flow.from_client_secrets_file(
                client_secrets_file=path,
                scopes=self.scopes,
                redirect_uri=os.path.join(request.host_url, self.callback_endpoint[1:]),
            )
        return self._flow

    def before_request(self):
        # NOTE: Hacking this in as we're forcing SSL below. Without this, all
        # request.{url,base_url} calls will use http incorrectly when assembling
        # oauth redirect URLs.
        request.scheme = 'https'

    def login_page(self):
        authorization_url, state = self.flow.authorization_url()
        session["state"] = state
        return redirect(authorization_url)
    
    def callback_page(self):
        if not session["state"] == request.args["state"]:
            abort(500)

        self.flow.fetch_token(authorization_response=request.url)
        credentials = self.flow.credentials
        token_request = google.auth.transport.requests.Request()

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=self.flow.client_config['client_id']
        )

        session["google_id"] = id_info.get("sub")  #defing the results to show on the page
        session["name"] = id_info.get("name")
        return redirect(self.login_redirect)  #the final page where the authorized users will end up
    
    def logout_page(self):
        session.clear()
        return redirect(self.logout_redirect)  #the final page where the unauthorized users will end up