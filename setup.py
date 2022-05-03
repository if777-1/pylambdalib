from setuptools import find_packages
from setuptools import setup
setup(
name='pylambdalib',
version='1.2.4',
description='Python package for Lambda Solution operations',
url='https://github.com/thcabrera/pylambdalib',
author='Thiago Cabrera Lavezzi',
author_email='thiagomartincabreralavezzi@gmail.com',
license='Lambda Solution',
install_requires=['shapely'],
packages=find_packages(),
zip_safe=False
)
