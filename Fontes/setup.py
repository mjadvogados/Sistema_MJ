from Cython.Build import cythonize

cythonize(
    "VHDX.pyx",
    compiler_directives={"language_level": "3"},
    build_dir="build"
)
