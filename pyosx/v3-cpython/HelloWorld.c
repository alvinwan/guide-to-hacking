#include <dlfcn.h>
#include <Python.h>
#include <stdio.h>

static PyObject* sayHello(PyObject* self, PyObject* args) {
    // Load the Objective-C dynamic library
    void* handle = dlopen("HelloWorld.dylib", RTLD_LAZY);
    
    // Load and call the function
    void (*func)() = dlsym(handle, "sayHello");
    func();
    
    // Cleanup
    dlclose(handle);
    Py_RETURN_NONE;
}

static PyMethodDef methods[] = {
    {"sayHello", sayHello, METH_NOARGS, "Call Objective-C sayHello."},
};

static struct PyModuleDef HelloWorld_module = {
    PyModuleDef_HEAD_INIT,
    "HelloWorld",  // Name of the module
    NULL,     // Documentation string
    -1,       // Size of per-interpreter state of the module
    methods
};

PyMODINIT_FUNC PyInit_HelloWorld(void) {
    return PyModule_Create(&HelloWorld_module);
}
