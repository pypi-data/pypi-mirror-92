from setuptools import setup, Extension
import os
import numpy


ext = Extension(
    "pymangle._mangle", ["pymangle/_mangle.c",
                         "pymangle/mangle.c",
                         "pymangle/cap.c",
                         "pymangle/polygon.c",
                         "pymangle/pixel.c",
                         "pymangle/point.c",
                         "pymangle/stack.c",
                         "pymangle/rand.c"],
    include_dirs=[numpy.get_include()],
)


exec(open('pymangle/version.py').read())

description = "A python code to read and work with mangle masks"

desc_file = os.path.join('README.md')
with open('README.md') as fobj:
    long_description = fobj.read()

setup(
    name="pymangle",
    packages=['pymangle'],
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=__version__,
    license="GPL",
    ext_modules=[ext],
    url="https://github.com/esheldon/pymangle",
    include_dirs=numpy.get_include(),
)
