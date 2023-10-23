```
# Build the dynamic library
clang -dynamiclib -framework Foundation HelloWorld.m -o HelloWorld.dylib

# Run the Python script
python hello_world.py
```