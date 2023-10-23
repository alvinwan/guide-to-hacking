#include <dlfcn.h>
#include <Python.h>
#include <stdio.h>

// Create a C function that wraps the Objective-C sayHello
static PyObject* sayHello(PyObject* self, PyObject* args) {
    // Load the Objective-C dynamic library
    void* handle = dlopen("HelloWorld.dylib", RTLD_LAZY);
    if (!handle) {
        printf("HelloWorld.dylib shared library was not found.");
        return NULL;
    }
    
    // Load and call the function
    void (*func)() = dlsym(handle, "sayHello");
    if (!func) {
        printf("sayHello function was not found.");
        return NULL;
    }
    func();
    
    // Cleanup
    dlclose(handle);
    Py_RETURN_NONE;
}

// Define metadata for the *Python sayHello function
static PyMethodDef methods[] = {
    {"sayHello", sayHello, METH_NOARGS, "Says 'Hello, World!'"},
};

// Define metadata for the *Python HelloWorld module
static struct PyModuleDef HelloWorld_module = {
    PyModuleDef_HEAD_INIT,
    "HelloWorld",   // Name of the module
    NULL,           // Documentation string
    -1,             // Size of per-interpreter state of the module
    methods
};

// Initialize both the HelloWorld module and sayHello function
PyMODINIT_FUNC PyInit_HelloWorld(void) {
    return PyModule_Create(&HelloWorld_module);
}
