from setuptools import setup

OPTIONS = {
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
    setup_requires=['py2app', 'pywebview', 'qtpy', 'pyqt6', 'PyQt6-WebEngine'],
    data_files=['client_secrets.json'],
)