from setuptools import setup

OPTIONS = {
    'argv_emulation': True,  # pass sys.argv to the app
    'strip': True,  # strip binaries
    'includes': ['WebKit', 'Foundation', 'webview'],
    'plist': {
        'CFBundleURLTypes': [  # for custom URL schemes (i.e., deeplinks)
            {
                'CFBundleURLName': 'MyApplication',  # arbitrary
                'CFBundleURLSchemes': ['myapp'],  # deeplink will be myapp://
            },
        ],
    },
}

setup(
    app=['app.py'],  # your main application
    options={'py2app': OPTIONS},
    setup_requires=['py2app', 'pywebview'],  # add other dependencies here
)