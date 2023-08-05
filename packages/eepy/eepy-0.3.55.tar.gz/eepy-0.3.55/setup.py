
import setuptools
from eepy import __version__ as APPVERSION
from eepy.cat import pycatcmd

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eepy",
    version=APPVERSION,
    author="H.B. Min",
    author_email="min.skku@gmail.com",
    url="https://github.com/hbmin/eepy",
    description="Package for a Python course",
    license="GNU General Public License v3 (GPLv3)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            '{} = eepy.cat:_main'.format(pycatcmd),
        ],
    },
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",

        # Indicate who your project is intended for
        "Intended Audience :: Education",
        "Topic :: Education",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",

        "Operating System :: OS Independent",
    ],
)

