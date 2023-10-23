```
# Build the dynamic library
clang -dynamiclib -o HelloWorld.dylib HelloWorld.m -framework Foundation

# Setup the CPython extension
pip install -e .

# Run the Python script
python hello_world.py
```