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
            
            Py_INCREF(marker);
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


static PyObject* zoom_path(PyObject* self, PyObject* args) {    // (list[GeoCoord], distance: double) -> list[GeoCoord]
    PyObject* path = NULL;
    double distance = 0.0f;

    if(!PyArg_ParseTuple(args, "Od", &path, &distance))
        return NULL;

    //if(!PyList_Check(path)) {
    //    PyErr_SetString(PyExc_TypeError, "parameter must be list.");
    //    return NULL;
    //}

    double distance2 = distance * distance;

    vector<GeoCoord> zoomed_path;
    zoomed_path.reserve(PyList_Size(path));

    PyObject* start = PyList_GetItem(path, 0);
    PyObject* lat = PyObject_GetAttrString(start, "lat");
    PyObject* lon = PyObject_GetAttrString(start, "lng");
    GeoCoord pivot { PyFloat_AsDouble(lat), PyFloat_AsDouble(lon) };
    Py_DECREF(lat);
    Py_DECREF(lon);
    zoomed_path.push_back(pivot);

    for(Py_ssize_t i = 1; i < PyList_Size(path); i++) {
        PyObject* marker = PyList_GetItem(path, i);

        //if(!PyObject_HasAttrString(marker, "lat") || !PyObject_HasAttrString(marker, "lng")) {
        //    PyErr_SetString(PyExc_TypeError, "parameter must be GeoCoord object.");
        //    return nullptr;
        //}

        PyObject* lat = PyObject_GetAttrString(marker, "lat");
        PyObject* lon = PyObject_GetAttrString(marker, "lng");

        GeoCoord marker_gc { PyFloat_AsDouble(lat), PyFloat_AsDouble(lon) };

        Py_DECREF(lat);
        Py_DECREF(lon);

        if(pivot.distance2(marker_gc) >= distance2) {
            pivot = marker_gc;
            zoomed_path.push_back(pivot);
        }
    }

    PyObject* last = PyList_GetItem(path, PyList_Size(path) - 1);
    lat = PyObject_GetAttrString(last, "lat");
    lon = PyObject_GetAttrString(last, "lng");
    GeoCoord last_gc { PyFloat_AsDouble(lat), PyFloat_AsDouble(lon) };
    Py_DECREF(lat);
    Py_DECREF(lon);
    zoomed_path.push_back(last_gc);

    PyObject* result = PyList_New(zoomed_path.size());    // list[GeoCoord]

    for(size_t i = 0; i < zoomed_path.size(); i++) {
        PyObject* marker = PyObject_CallFunction(PyObject_GetAttrString(PyImport_ImportModule("charger"), "GeoCoord"), "dd", zoomed_path[i].lat, zoomed_path[i].lon);
        PyList_SetItem(result, i, marker);
    }

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
    { "zoom_path", zoom_path, METH_VARARGS, "zoom path. 근데 더 느리다.." },
    { "sort_by_distance", sort_by_distance, METH_VARARGS, "sort list. 얘도 더 느리다.." },
    { "only_in_map", only_in_map, METH_VARARGS, "filter markers. 얘는 별 차이가 없다..." },
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
