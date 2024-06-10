#include "python.h" 

#include <string>
#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;


struct GeoCoord {
    long double lat;
    long double lon;
};


static PyObject* spam_hello(PyObject* self, PyObject* args) {
    return PyUnicode_FromString("Hello, world!");
}


static PyObject* pass_GeoCoord(PyObject* self, PyObject* args) {
    PyObject* coord = nullptr;      // python GeoCoord ��ü�� ���� ����
    GeoCoord gc;                    // C++ GeoCoord ��ü�� ���� ����

    // ���̽㿡�� GeoCoord ��ü�� �޾ƿ´�.
    if(!PyArg_ParseTuple(args, "O", &coord))
        return nullptr;

    // ���̽� ��ü�� GeoCoord ��ü�� �´��� Ȯ���Ѵ�.
    if(!PyObject_HasAttrString(coord, "lat") || !PyObject_HasAttrString(coord, "lng")) {
        PyErr_SetString(PyExc_TypeError, "parameter must be GeoCoord object.");
        return nullptr;
    }

    // ���̽� ��ü���� lat, lon ���� �޾ƿ´�.
    PyObject* lat = PyObject_GetAttrString(coord, "lat");
    PyObject* lon = PyObject_GetAttrString(coord, "lng");

    // lat, lon ���� C++ GeoCoord ��ü�� �ִ´�.
    gc.lat = PyFloat_AsDouble(lat);
    gc.lon = PyFloat_AsDouble(lon);

    // ���̽� ��ü���� �޾ƿ� ���۷����� �����Ѵ�.
    Py_DECREF(lat);
    Py_DECREF(lon);

    // C++ GeoCoord ��ü�� ����Ѵ�.
    cout << "lat: " << gc.lat << ", lon: " << gc.lon << endl;
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
    { "pass_GeoCoord", pass_GeoCoord, METH_VARARGS, "pass GeoCoord" },
    { "sort", spam_sort, METH_VARARGS, "sort list." },
    { NULL, NULL, 0, NULL } // �迭�� ���� ��Ÿ���ϴ�.
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "sidekick",            // ��� �̸�
    "- hello\n- sort", // ��� ������ ���� �κ�, ����� __doc__�� ����˴ϴ�.
    -1,
    SpamMethods
};

PyMODINIT_FUNC PyInit_sidekick(void) {
    return PyModule_Create(&spammodule);
}
