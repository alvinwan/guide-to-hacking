#include <dlfcn.h>
#include <Python.h>
#include <stdio.h>

static PyObject* getFirstEntry(PyObject* self, PyObject* args) {
    // Load the Objective-C dynamic library
    void* handle = dlopen("Book.dylib", RTLD_LAZY);
    if (!handle) {
        printf("Book.dylib shared library was not found.");
        return NULL;
    }

    // Load and call the function
    const char* (*func)() = dlsym(handle, "getAddressBookFirstEntry");
    if (!func) {
        printf("getAddressBookFirstEntry function was not found.");
        return NULL;
    }
    const char* display = func();
    
    // Cleanup
    dlclose(handle);
    return Py_BuildValue("s", display); // Build Python string object
}

static PyMethodDef methods[] = {
    {"getFirstEntry", getFirstEntry, METH_VARARGS, "List first entry"},
};

static struct PyModuleDef Book_module = {
    PyModuleDef_HEAD_INIT,
    "Book",   // Name of the module
    NULL,     // Documentation string
    -1,       // Size of per-interpreter state of the module
    methods
};

PyMODINIT_FUNC PyInit_Book(void) {
    return PyModule_Create(&Book_module);
}
