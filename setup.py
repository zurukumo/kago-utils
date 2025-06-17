from setuptools import Extension, find_packages, setup

setup(
    name="kago_utils",
    packages=find_packages(),
    package_data={"kago_utils": ["py.typed"]},
    include_package_data=True,
    exclude_package_data={"kago_utils": ["resources/distance_tables/*.c"]},
    ext_modules=[
        Extension(
            name="kago_utils.ext._shanten",
            sources=["kago_utils/ext/_shanten.c"],
        ),
    ],
)
