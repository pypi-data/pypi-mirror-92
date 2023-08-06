"""
opod is a an orhestrator for Podman.
Copyright (C) 2021  Brian Farrell

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact: brian.farrell@me.com
"""

from setuptools import setup, find_packages

from opod.__version__ import __version__, _version_min_python_

with open("README.rst", "r") as fh:
    long_description = fh.read()


setup(
    name='opod',
    version=__version__,
    python_requires=f">={_version_min_python_}",

    packages=find_packages(),

    license='AGPLv3',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
    ],

    url='https://pypi.org/project/opod/',
    author="Brian Farrell",
    author_email="brian.farrell@me.com",
    description="Use opod orchestrate Podman",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    keywords="Podman docker-compose orchestration",
    entry_points={
        "console_scripts": [
            "opod=opod:main",
        ],
    },
    zip_safe=False,
)
