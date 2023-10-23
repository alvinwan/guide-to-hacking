from setuptools import Extension, setup

# Below, 'Say' is the name you'll import in Python
setup(ext_modules=[Extension("Book", ["Book.c"])])