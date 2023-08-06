"""Setup script for gcloudbearer"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="bearer-gencloud",
    version="1.0.0",
    description="Token generator for cloud endpoints",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/BrunoTSBuzzo/gcloudbearer",
    author="Bruno Buzzo",
    author_email="brunobuzzo.dev@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["gcloudbearer"],
    include_package_data=True,
    install_requires=[
        "google-auth",
    ],
    entry_points={"console_scripts": ["generate_headers=gcloudbearer.__main__:main"]},
)
