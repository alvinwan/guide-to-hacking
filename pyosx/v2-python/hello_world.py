import ctypes
import ctypes.util

# Load the dynamic library
hello_lib = ctypes.CDLL('HelloWorld.dylib')

# Initialize the Objective-C runtime
objc = ctypes.CDLL(ctypes.util.find_library('objc'))

# Declare the "prototype" (e.g., datatypes) for sayHello
sayHello = hello_lib.sayHello
sayHello.argtypes = None
sayHello.restype = None

# Call the sayHello function
sayHello()
