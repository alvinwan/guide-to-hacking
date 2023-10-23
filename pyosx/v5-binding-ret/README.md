To directly run the Objective-C say script with demo inputs
```
clang -framework Foundation -framework AddressBook Book.m -o book && ./book
```

To run the Python script

```
# Build the dynamic library and the CPython extension
clang -dynamiclib -o Book.dylib Book.m -framework Foundation -framework AddressBook && pip install .

# Run the Python script
python book.py
```