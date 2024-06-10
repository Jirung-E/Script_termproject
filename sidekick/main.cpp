#include "python.h" 

#include <string>
#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;


static PyObject* spam_hello(PyObject* self, PyObject* args) {
    return PyUnicode_FromString("Hello, world!");
}


static PyObject* spam_sort(PyObject* self, PyObject* args) {
    PyObject* list = NULL;

    if(!PyArg_ParseTuple(args, "O", &list))
        return NULL;

    if(!PyList_Check(list)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be list.");
        return NULL;
    }

    vector<int> v;

    for(Py_ssize_t i = 0; i < PyList_Size(list); i++) {
        PyObject* item = PyList_GetItem(list, i);
        if(!PyLong_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "list must be integer list.");
            return NULL;
        }

        v.push_back(PyLong_AsLong(item));
    }

    sort(v.begin(), v.end());

    PyObject* ret = PyList_New(v.size());

    for(Py_ssize_t i = 0; i < v.size(); i++) {
        PyObject* item = PyLong_FromLong(v[i]);
        PyList_SetItem(ret, i, item);
    }

    return ret;
}


static PyMethodDef SpamMethods[] = {
    { "hello", spam_hello, METH_VARARGS, "say hello" },
    { "sort", spam_sort, METH_VARARGS, "sort list." },
    { NULL, NULL, 0, NULL } // 배열의 끝을 나타냅니다.
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "sidekick",            // 모듈 이름
    "- hello\n- sort", // 모듈 설명을 적는 부분, 모듈의 __doc__에 저장됩니다.
    -1,
    SpamMethods
};

PyMODINIT_FUNC PyInit_sidekick(void) {
    return PyModule_Create(&spammodule);
}
