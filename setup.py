from setuptools import find_packages
from setuptools import setup
import platform

required_packages = ['shapely', # for shapes
                     'scipy', # for search trees
                     'ezdxf', # for DXF files
                     'simplekml', # for kml files
                     'openpyxl', # for xlxs files
                     'python-dotenv'
                     ]

linux_only = ['redis', # to connect to redis
              ]

if platform.system() == "Linux":
    required_packages.extend(linux_only)

setup(
name='pylambdalib',
version='1.5.1',
description='Python package for Lambda Solution operations',
url='https://github.com/thcabrera/pylambdalib',
author='Thiago Cabrera Lavezzi',
author_email='thiagomartincabreralavezzi@gmail.com',
license='Lambda Solution',
install_requires=required_packages,
packages=find_packages(),
zip_safe=False
)

