#define PY_SSIZE_T_CLEAN
#include "../resources/distance_tables/suuhai_distance_table.c"
#include "../resources/distance_tables/zihai_distance_table.c"
#include <Python.h>
#include <stdbool.h>

static int get_length_key(int length) {
  if (length % 3 == 2) {
    return (length - 2) * 2 / 3;
  } else {
    return (length - 3) * 2 / 3 + 1;
  }
}

static int get_pattern_key(const int *pattern, int len) {
  int k = 0;
  for (int i = 0; i < len; ++i) {
    k = k * 5 + pattern[i];
  }
  return k;
}

static PyObject *calculate_regular_shanten(PyObject *self, PyObject *args) {
  PyObject *counter_obj;
  if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &counter_obj)) {
    return NULL;
  }

  int manzu_pattern[9] = {0};
  int pinzu_pattern[9] = {0};
  int souzu_pattern[9] = {0};
  int zihai_pattern[7] = {0};
  int total = 0;

  for (int i = 0; i < 9; ++i) {
    manzu_pattern[i] = PyLong_AsLong(PyList_GetItem(counter_obj, i));
    total += manzu_pattern[i];
  }
  for (int i = 0; i < 9; ++i) {
    pinzu_pattern[i] = PyLong_AsLong(PyList_GetItem(counter_obj, i + 9));
    total += pinzu_pattern[i];
  }
  for (int i = 0; i < 9; ++i) {
    souzu_pattern[i] = PyLong_AsLong(PyList_GetItem(counter_obj, i + 18));
    total += souzu_pattern[i];
  }
  for (int i = 0; i < 7; ++i) {
    zihai_pattern[i] = PyLong_AsLong(PyList_GetItem(counter_obj, i + 27));
    total += zihai_pattern[i];
  }

  int n_menstu = total / 3;
  int manzu_pattern_key = get_pattern_key(manzu_pattern, 9);
  int pinzu_pattern_key = get_pattern_key(pinzu_pattern, 9);
  int souzu_pattern_key = get_pattern_key(souzu_pattern, 9);
  int zihai_pattern_key = get_pattern_key(zihai_pattern, 7);

  int min_shanten = 8;

  for (int n_manzu_mentsu = 0; n_manzu_mentsu <= n_menstu; ++n_manzu_mentsu) {
    for (int n_pinzu_mentsu = 0; n_pinzu_mentsu <= n_menstu - n_manzu_mentsu; ++n_pinzu_mentsu) {
      for (int n_souzu_mentsu = 0; n_souzu_mentsu <= n_menstu - n_manzu_mentsu - n_pinzu_mentsu; ++n_souzu_mentsu) {
        int n_zihai_mentsu = n_menstu - n_manzu_mentsu - n_pinzu_mentsu - n_souzu_mentsu;
        for (int n_manzu_jantou = 0; n_manzu_jantou <= 1; ++n_manzu_jantou) {
          for (int n_pinzu_jantou = 0; n_pinzu_jantou <= 1 - n_manzu_jantou; ++n_pinzu_jantou) {
            for (int n_souzu_jantou = 0; n_souzu_jantou <= 1 - n_manzu_jantou - n_pinzu_jantou; ++n_souzu_jantou) {
              int n_zihai_jantou = 1 - n_manzu_jantou - n_pinzu_jantou - n_souzu_jantou;

              int manzu_length = n_manzu_mentsu * 3 + n_manzu_jantou * 2;
              int pinzu_length = n_pinzu_mentsu * 3 + n_pinzu_jantou * 2;
              int souzu_length = n_souzu_mentsu * 3 + n_souzu_jantou * 2;
              int zihai_length = n_zihai_mentsu * 3 + n_zihai_jantou * 2;

              int manzu_distance =
                  manzu_length == 0 ? 0 : suuhai_table[get_length_key(manzu_length)][manzu_pattern_key];
              int pinzu_distance =
                  pinzu_length == 0 ? 0 : suuhai_table[get_length_key(pinzu_length)][pinzu_pattern_key];
              int souzu_distance =
                  souzu_length == 0 ? 0 : suuhai_table[get_length_key(souzu_length)][souzu_pattern_key];
              int zihai_distance =
                  zihai_length == 0 ? 0 : zihai_table[get_length_key(zihai_length)][zihai_pattern_key];

              int shanten = manzu_distance + pinzu_distance + souzu_distance + zihai_distance - 1;
              if (shanten < min_shanten)
                min_shanten = shanten;
            }
          }
        }
      }
    }
  }

  return PyLong_FromLong(min_shanten);
}

static PyObject *calculate_chiitoitsu_shanten(PyObject *self, PyObject *args) {
  PyObject *counter_obj;
  if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &counter_obj)) {
    return NULL;
  }

  int counter[34], total = 0;
  for (int i = 0; i < 34; ++i) {
    counter[i] = PyLong_AsLong(PyList_GetItem(counter_obj, i));
    total += counter[i];
  }
  if (total < 13 || total > 14)
    return PyLong_FromLong(9999);

  int n_toitsu = 0, n_unique_hai = 0;
  for (int i = 0; i < 34; ++i) {
    if (counter[i] >= 2)
      n_toitsu++;
    if (counter[i] >= 1)
      n_unique_hai++;
  }

  int result = 6 - n_toitsu + ((n_unique_hai < 7) ? (7 - n_unique_hai) : 0);
  return PyLong_FromLong(result);
}

static PyObject *calculate_kokushimusou_shanten(PyObject *self, PyObject *args) {
  PyObject *counter_obj;
  if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &counter_obj)) {
    return NULL;
  }

  int counter[34], total = 0;
  for (int i = 0; i < 34; ++i) {
    counter[i] = PyLong_AsLong(PyList_GetItem(counter_obj, i));
    total += counter[i];
  }
  if (total < 13 || total > 14)
    return PyLong_FromLong(9999);

  int yaochu_hais[] = {
      0,  8,                     // 1m, 9m
      9,  17,                    // 1p, 9p
      18, 26,                    // 1s, 9s
      27, 28, 29, 30, 31, 32, 33 // 1z - 7z
  };
  int n_yaochu_hai = 0;
  bool has_toitsu = false;
  for (int i = 0; i < 13; ++i) {
    int idx = yaochu_hais[i];
    if (counter[idx] >= 1)
      n_yaochu_hai++;
    if (counter[idx] >= 2)
      has_toitsu = true;
  }

  int result = 13 - n_yaochu_hai - (has_toitsu ? 1 : 0);
  return PyLong_FromLong(result);
}

static PyMethodDef ShantenMethods[] = {
    {"calculate_regular_shanten", calculate_regular_shanten, METH_VARARGS, "Calculate regular shanten number"},
    {"calculate_chiitoitsu_shanten", calculate_chiitoitsu_shanten, METH_VARARGS, "Calculate chiitoitsu shanten"},
    {"calculate_kokushimusou_shanten", calculate_kokushimusou_shanten, METH_VARARGS, "Calculate kokushimusou shanten"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef shantenmodule = {PyModuleDef_HEAD_INIT, "_shanten", NULL, -1, ShantenMethods};

PyMODINIT_FUNC PyInit__shanten(void) { return PyModule_Create(&shantenmodule); }
