#include "python.h" 

#include <string>
#include <iostream>
#include <algorithm>
#include <vector>
#include <deque>

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
    GeoCoord(const GeoCoord& other) : lat { other.lat }, lon { other.lon } {

    }

    GeoCoord& operator=(const GeoCoord& other) {
        lat = other.lat;
        lon = other.lon;

        return *this;
    }

public:
    double distance2(const GeoCoord& other) const {
        double lat_diff = lat - other.lat;
        double lon_diff = lon - other.lon;

        return lat_diff * lat_diff + lon_diff * lon_diff;
    }
};


static PyObject* furthest_marker(PyObject* self, PyObject* args) {
    PyObject* coord = nullptr;
    PyObject* markers = nullptr;

    if(!PyArg_ParseTuple(args, "OO", &coord, &markers))
        return nullptr;

    PyObject* lat = PyObject_GetAttrString(coord, "lat");
    PyObject* lon = PyObject_GetAttrString(coord, "lng");

    GeoCoord gc { PyFloat_AsDouble(lat), PyFloat_AsDouble(lon) };

    Py_DECREF(lat);
    Py_DECREF(lon);

    double max_distance2 = 0.0f;
    PyObject* max_marker = nullptr;
    long max_index = -1;

    for(Py_ssize_t i = 0; i < PyList_Size(markers); i++) {
        PyObject* marker = PyList_GetItem(markers, i);

        PyObject* lat = PyObject_GetAttrString(marker, "lat");
        PyObject* lon = PyObject_GetAttrString(marker, "lng");

        GeoCoord marker_gc { PyFloat_AsDouble(lat), PyFloat_AsDouble(lon) };

        Py_DECREF(lat);
        Py_DECREF(lon);

        double distance2 = gc.distance2(marker_gc);

        if(distance2 > max_distance2) {
            max_distance2 = distance2;
            max_marker = marker;
            max_index = i;
        }
    }

    PyObject* idx = PyLong_FromLong(max_index);
    PyObject* result = PyTuple_Pack(2, idx, max_marker);
    //Py_INCREF(max_marker);

    return result;
}


static PyObject* only_in_map(PyObject* self, PyObject* args) {    // (list[GeoCoord], center: GeoCoord, distance: double) -> list[GeoCoord]
    PyObject* markers = nullptr;
    PyObject* center = nullptr;
    double distance = 0.0;

    if(!PyArg_ParseTuple(args, "OOd", &markers, &center, &distance))
        return nullptr;

    PyObject* lat = PyObject_GetAttrString(center, "lat");
    PyObject* lon = PyObject_GetAttrString(center, "lng");

    GeoCoord center_gc { PyFloat_AsDouble(lat), PyFloat_AsDouble(lon) };

    Py_DECREF(lat);
    Py_DECREF(lon);

    PyObject* result = PyList_New(0);

    for(Py_ssize_t i = 0; i < PyList_Size(markers); i++) {
        PyObject* marker = PyList_GetItem(markers, i);

        PyObject* lat = PyObject_GetAttrString(marker, "lat");
        PyObject* lon = PyObject_GetAttrString(marker, "lng");

        GeoCoord marker_gc { PyFloat_AsDouble(lat), PyFloat_AsDouble(lon) };

        Py_DECREF(lat);
        Py_DECREF(lon);

        if(abs(center_gc.lat - marker_gc.lat) < distance && abs(center_gc.lon - marker_gc.lon) < distance) {
            PyList_Append(result, marker);
            Py_INCREF(marker);
        }
    }

    return result;
}


static PyMethodDef SpamMethods[] = {
    { "furthest_marker", furthest_marker, METH_VARARGS, "find furthest marker. 얘는 빠르다." },
    { "only_in_map", only_in_map, METH_VARARGS, "filter markers. 얘는 별 차이가 없거나 조금 더 느리다..." },
    { NULL, NULL, 0, NULL } // 배열의 끝을 나타냅니다.
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "sidekick",
    "- furthest_marker\n- only_in_map\n",
    -1,
    SpamMethods
};

PyMODINIT_FUNC PyInit_sidekick(void) {
    return PyModule_Create(&spammodule);
}
