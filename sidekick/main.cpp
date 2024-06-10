#include "python.h" 

#include <string>
#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;


class GeoCoord {
public:
    double lat;
    double lon;

public:
    GeoCoord(double lat, double lon) : lat { lat }, lon { lon } {

    }
    GeoCoord() : lat { 0.0f }, lon { 0.0f } {

    }

public:
    double distance2(const GeoCoord& other) const {
        double lat_diff = lat - other.lat;
        double lon_diff = lon - other.lon;

        return lat_diff * lat_diff + lon_diff * lon_diff;
    }
};


static PyObject* spam_hello(PyObject* self, PyObject* args) {
    return PyUnicode_FromString("Hello, world!");
}


static PyObject* pass_GeoCoord(PyObject* self, PyObject* args) {
    PyObject* coord = nullptr;      // python GeoCoord 객체를 받을 변수
    GeoCoord gc;                    // C++ GeoCoord 객체를 만들 변수

    // 파이썬에서 GeoCoord 객체를 받아온다.
    if(!PyArg_ParseTuple(args, "O", &coord))
        return nullptr;

    // 파이썬 객체가 GeoCoord 객체가 맞는지 확인한다.
    if(!PyObject_HasAttrString(coord, "lat") || !PyObject_HasAttrString(coord, "lng")) {
        PyErr_SetString(PyExc_TypeError, "parameter must be GeoCoord object.");
        return nullptr;
    }

    // 파이썬 객체에서 lat, lon 값을 받아온다.
    PyObject* lat = PyObject_GetAttrString(coord, "lat");
    PyObject* lon = PyObject_GetAttrString(coord, "lng");

    // lat, lon 값을 C++ GeoCoord 객체에 넣는다.
    gc.lat = PyFloat_AsDouble(lat);
    gc.lon = PyFloat_AsDouble(lon);

    // 파이썬 객체에서 받아온 레퍼런스를 해제한다.
    Py_DECREF(lat);
    Py_DECREF(lon);

    // C++ GeoCoord 객체를 출력한다.
    cout << "lat: " << gc.lat << ", lon: " << gc.lon << endl;
}


static PyObject* distance2_between(PyObject* self, PyObject* args) {
    PyObject* coord1 = nullptr;
    PyObject* coord2 = nullptr;

    if(!PyArg_ParseTuple(args, "OO", &coord1, &coord2))
        return nullptr;

    //if(!PyObject_HasAttrString(coord1, "lat") || !PyObject_HasAttrString(coord1, "lng") ||
    //   !PyObject_HasAttrString(coord2, "lat") || !PyObject_HasAttrString(coord2, "lng")) {
    //    PyErr_SetString(PyExc_TypeError, "parameter must be GeoCoord object.");
    //    return nullptr;
    //}

    PyObject* lat1 = PyObject_GetAttrString(coord1, "lat");
    PyObject* lon1 = PyObject_GetAttrString(coord1, "lng");
    PyObject* lat2 = PyObject_GetAttrString(coord2, "lat");
    PyObject* lon2 = PyObject_GetAttrString(coord2, "lng");

    GeoCoord gc1 { PyFloat_AsDouble(lat1), PyFloat_AsDouble(lon1) };
    GeoCoord gc2 { PyFloat_AsDouble(lat2), PyFloat_AsDouble(lon2) };

    Py_DECREF(lat1);
    Py_DECREF(lon1);
    Py_DECREF(lat2);
    Py_DECREF(lon2);

    return PyFloat_FromDouble(gc1.distance2(gc2));
}


static PyObject* furthest_marker(PyObject* self, PyObject* args) {
    PyObject* coord = nullptr;
    PyObject* markers = nullptr;

    if(!PyArg_ParseTuple(args, "OO", &coord, &markers))
        return nullptr;

    //if(!PyObject_HasAttrString(coord, "lat") || !PyObject_HasAttrString(coord, "lng")) {
    //    PyErr_SetString(PyExc_TypeError, "parameter must be GeoCoord object.");
    //    return nullptr;
    //}

    //if(!PyList_Check(markers)) {
    //    PyErr_SetString(PyExc_TypeError, "parameter must be list.");
    //    return nullptr;
    //}

    PyObject* lat = PyObject_GetAttrString(coord, "lat");
    PyObject* lon = PyObject_GetAttrString(coord, "lng");

    GeoCoord gc { PyFloat_AsDouble(lat), PyFloat_AsDouble(lon) };

    Py_DECREF(lat);
    Py_DECREF(lon);

    double max_distance2 = 0.0f;
    PyObject* max_marker = nullptr;

    for(Py_ssize_t i = 0; i < PyList_Size(markers); i++) {
        PyObject* marker = PyList_GetItem(markers, i);

        //if(!PyObject_HasAttrString(marker, "lat") || !PyObject_HasAttrString(marker, "lng")) {
        //    PyErr_SetString(PyExc_TypeError, "parameter must be GeoCoord object.");
        //    return nullptr;
        //}

        PyObject* lat = PyObject_GetAttrString(marker, "lat");
        PyObject* lon = PyObject_GetAttrString(marker, "lng");

        GeoCoord marker_gc { PyFloat_AsDouble(lat), PyFloat_AsDouble(lon) };

        Py_DECREF(lat);
        Py_DECREF(lon);

        double distance2 = gc.distance2(marker_gc);

        if(distance2 > max_distance2) {
            max_distance2 = distance2;
            max_marker = marker;
        }
    }

    return max_marker;
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
    { "distance2_between", distance2_between, METH_VARARGS, "distance2 between two GeoCoord" },
    { "furthest_marker", furthest_marker, METH_VARARGS, "find furthest marker" },
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
