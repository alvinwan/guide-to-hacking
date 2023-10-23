from setuptools import Extension, setup

# Below, 'HelloWorld' is the name you'll import in Python
setup(ext_modules=[Extension("HelloWorld", ["HelloWorld.c"])])