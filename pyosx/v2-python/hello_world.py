import ctypes
import ctypes.util

# Load the dynamic library
hello_lib = ctypes.CDLL('HelloWorld.dylib')

# Initialize the Objective-C runtime
objc = ctypes.CDLL(ctypes.util.find_library('objc'))

# Declare the function prototype for sayHello
sayHello = hello_lib.sayHello
sayHello.argtypes = None
sayHello.restype = None

# Call the sayHello function
sayHello()

# NOTE: For classes and their methods, use their mangled names. See the code
# snippet below for working with those.

# objc.objc_getClass.restype = ctypes.c_void_p  # Define runtime types
# objc.sel_registerName.restype = ctypes.c_void_p
# objc.objc_msgSend.restype = ctypes.c_void_p
# objc.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

# class_ptr = objc.objc_getClass(b'HelloWorld')  # Note the 'b' before the string
# method_sel = objc.sel_registerName(b'sayHello')
# obj = objc.objc_msgSend(class_ptr, objc.sel_registerName(b'new'))  # instantiate
# objc.objc_msgSend(obj, method_sel)  # Call the method
