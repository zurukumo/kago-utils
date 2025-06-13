from setuptools import Extension, setup

setup(
    ext_modules=[
        Extension(
            name="kago_utils.ext._shanten",
            sources=["kago_utils/ext/_shanten.c"],
        ),
    ]
)
