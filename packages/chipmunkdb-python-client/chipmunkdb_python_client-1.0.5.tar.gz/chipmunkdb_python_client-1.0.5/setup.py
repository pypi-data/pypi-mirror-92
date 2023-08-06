"""Setup script for chipmunkdb_python_client"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README_pip.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="chipmunkdb_python_client",
    version="1.0.5",
    description="Read and Write Dataframes and Data to a chipmunkdb",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/coindeck/chipmunkdb-python-client",
    author="coindeck",
    author_email="donnercody86@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["chipmunkdb"],
    include_package_data=True,
    install_requires=[
        "requests", "pandas", "influxdb", "importlib_resources", "typing"
    ],
    entry_points={"console_scripts": ["chipmunkdb_python_client=chipmunkdb.ChipmunkDb:main"]},
)