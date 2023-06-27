from setuptools import setup

setup(
    app=['app.py'],  # your main application
    setup_requires=['flask', 'py2app', 'pywebview'],  # add other dependencies here
)