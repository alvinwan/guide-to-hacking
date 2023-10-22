```
# Build the dynamic library
clang -dynamiclib -o HelloWorld.dylib HelloWorld.m -framework Foundation

# Run the Python script
python hello_world.py
```