#include <dlfcn.h>
#include <Python.h>
#include <stdio.h>

static PyObject* say(PyObject* self, PyObject* args) {
    // Load the Objective-C dynamic library
    void* handle = dlopen("Say.dylib", RTLD_LAZY);

    // Grab the string argument
    char* text;
    if (!PyArg_ParseTuple(args, "s", &text)) {
        return NULL;
    }

    // Load and call the function
    void (*func)(char*) = dlsym(handle, "say");
    func(text);
    
    // Cleanup
    dlclose(handle);
    Py_RETURN_NONE;
}

static PyMethodDef methods[] = {
    {"say", say, METH_VARARGS, "Call Objective-C say."},
};

static struct PyModuleDef Say_module = {
    PyModuleDef_HEAD_INIT,
    "Say",  // Name of the module
    NULL,     // Documentation string
    -1,       // Size of per-interpreter state of the module
    methods
};

PyMODINIT_FUNC PyInit_Say(void) {
    return PyModule_Create(&Say_module);
}
