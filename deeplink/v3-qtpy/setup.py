from setuptools import setup

OPTIONS = {  # notice argv_emulation has been removed
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
    app=['app.py'],
    options={'py2app': OPTIONS},
    setup_requires=['py2app', 'pyqt6'],  # add pyqt to dependencies
)