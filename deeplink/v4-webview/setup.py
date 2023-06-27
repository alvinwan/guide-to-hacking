"""Simple setup script for actually building your application. See README"""

from setuptools import setup

APP = ['app.py']  # your main application
OPTIONS = {
    # 'argv_emulation': True,  # pass sys.argv to the app
    'plist': {
        'CFBundleURLTypes': [  # for custom URL schemes (i.e., deeplinks)
            {
                'CFBundleURLName': 'MyApplication',  # arbitrary
                'CFBundleURLSchemes': ['myapp'],  # deeplink will be myapp://
            },
        ],
    },
    'strip': True,
    'includes': ['WebKit', 'Foundation', 'webview'],
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app', 'pyqt6'],  # add other dependencies here
)