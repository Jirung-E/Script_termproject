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


GeoCoord furthest_marker(const GeoCoord& coord, const vector<GeoCoord>& markers) {
    double max_distance2 = 0.0f;
    GeoCoord max_marker;

    for(const GeoCoord& marker : markers) {
        double distance2 = coord.distance2(marker);

        if(distance2 > max_distance2) {
            max_distance2 = distance2;
            max_marker = marker;
        }
    }

    return max_marker;
}


//static PyObject* grouped_markers(PyObject* self, PyObject* args) {
//    PyObject* markers = nullptr;
//    double radius = 0.0f;
//
//    if(!PyArg_ParseTuple(args, "Od", &markers, &radius))
//        return nullptr;
//
//    //if(!PyList_Check(markers)) {
//    //    PyErr_SetString(PyExc_TypeError, "parameter must be list.");
//    //    return nullptr;
//    //}
//
//    double radius2 = radius * radius;
//
//    Py_ssize_t size = PyList_Size(markers);
//    vector<GeoCoord> groups;
//    groups.reserve(size);
//    
//    PyObject* first = PyList_GetItem(markers, 0);
//    PyObject* lat = PyObject_GetAttrString(first, "lat");
//    PyObject* lon = PyObject_GetAttrString(first, "lng");
//    GeoCoord pivot { PyFloat_AsDouble(lat), PyFloat_AsDouble(lon) };
//
//    Py_DECREF(lat);
//    Py_DECREF(lon);
//}


static PyObject* sort_by_distance(PyObject* self, PyObject* args) {     // (list[GeoCoord], GeoCoord) -> list[GeoCoord]
    PyObject* list = NULL;
    PyObject* center = NULL;

    if(!PyArg_ParseTuple(args, "OO", &list, &center))
        return NULL;

    //if(!PyObject_HasAttrString(center, "lat") || !PyObject_HasAttrString(center, "lng")) {
    //    PyErr_SetString(PyExc_TypeError, "parameter must be GeoCoord object.");
    //    return NULL;
    //}

    PyObject* lat = PyObject_GetAttrString(center, "lat");
    PyObject* lon = PyObject_GetAttrString(center, "lng");

    GeoCoord center_gc { PyFloat_AsDouble(lat), PyFloat_AsDouble(lon) };

    Py_DECREF(lat);
    Py_DECREF(lon);

    //if(!PyList_Check(list)) {
    //    PyErr_SetString(PyExc_TypeError, "parameter must be list.");
    //    return NULL;
    //}

    vector<GeoCoord> v;
    v.reserve(PyList_Size(list));

    for(Py_ssize_t i = 0; i < PyList_Size(list); i++) {
        PyObject* marker = PyList_GetItem(list, i);

        //if(!PyObject_HasAttrString(marker, "lat") || !PyObject_HasAttrString(marker, "lng")) {
        //    PyErr_SetString(PyExc_TypeError, "parameter must be GeoCoord object.");
        //    return nullptr;
        //}

        PyObject* lat = PyObject_GetAttrString(marker, "lat");
        PyObject* lon = PyObject_GetAttrString(marker, "lng");

        GeoCoord marker_gc { PyFloat_AsDouble(lat), PyFloat_AsDouble(lon) };

        Py_DECREF(lat);
        Py_DECREF(lon);

        v.push_back(marker_gc);
    }

    sort(v.begin(), v.end(), [&](const GeoCoord& a, const GeoCoord& b) {
        return a.distance2(center_gc) < b.distance2(center_gc);
    });

    PyObject* result = PyList_New(v.size());    // list[GeoCoord]
    for(size_t i = 0; i < v.size(); i++) {
        PyObject* marker = PyObject_CallFunction(PyObject_GetAttrString(PyImport_ImportModule("charger"), "GeoCoord"), "dd", v[i].lat, v[i].lon);
        PyList_SetItem(result, i, marker);
    }

    return result;
}


static PyMethodDef SpamMethods[] = {
    { "furthest_marker", furthest_marker, METH_VARARGS, "find furthest marker" },
    { "sort_by_distance", sort_by_distance, METH_VARARGS, "sort list." },
    { NULL, NULL, 0, NULL } // 배열의 끝을 나타냅니다.
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "sidekick",
    "- furthest_marker\n- zoom_path\n- only_in_map\n- sort_by_distance\n",
    -1,
    SpamMethods
};

PyMODINIT_FUNC PyInit_sidekick(void) {
    return PyModule_Create(&spammodule);
}
