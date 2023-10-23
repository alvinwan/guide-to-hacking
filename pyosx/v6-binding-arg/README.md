To directly run the Objective-C say script with demo inputs
```
clang -framework Foundation -framework AVFoundation Say.m -o say && ./say
```

To run the Python script

```
# Build the dynamic library and the CPython extension
clang -dynamiclib -o Say.dylib Say.m -framework Foundation -framework AVFoundation && pip install -e .

# Run the Python script
python say.py
```