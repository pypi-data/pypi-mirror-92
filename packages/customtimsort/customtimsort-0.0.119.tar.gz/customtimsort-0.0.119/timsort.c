#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include <string.h>
#include <listobject.c>

int Get_minrun(char path[], int size_of_array)
{
    char line[30] = {0};
    int line_count = -3;

    FILE *file = fopen(path, "r");

    int first_size = 0, step = 1;
    int minrun = 2;
    while (fgets(line, 30, file))
    {
        if (line_count == -3) {
            first_size = atoi(line);
        } else if (line_count == -2) {
            step = atoi(line);
        } else if (line_count >= 0 && first_size + line_count * step == size_of_array) {
            minrun = atoi(line);
        }
        line_count++;
    }
    fclose(file);
    return minrun;
}

static PyObject *
timsort(PyObject *self, PyObject *args)
{
    PyObject * arr;
    Py_ssize_t minrun;
    if (!PyArg_ParseTuple(args, "nO", &minrun, &arr))
        return NULL;
    PyList_Custom_Sort(arr, minrun);
    return PyLong_FromLong(1);
}

static PyMethodDef TimSortMethods[] = {
    {"timsort",  timsort, METH_VARARGS,
     "Execute a shell command."},
    {"Get_minrun",  Get_minrun, METH_VARARGS,
     "Execute a shell command."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef timsort_module = {
    PyModuleDef_HEAD_INIT,
    "timsort",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    TimSortMethods
};

PyMODINIT_FUNC
PyInit_timsort(void)
{
    return PyModule_Create(&timsort_module);
}

