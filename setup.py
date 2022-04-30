from setuptools import find_packages
from setuptools import setup
setup(
name='pylambdalib',
version='1.0.0',
description='Python package for Lambda Solution operations',
url='#',
author='Thiago Cabrera Lavezzi',
author_email='thiagomartincabreralavezzi@gmail.com',
license='Lambda Solution',
install_requires=['shapely'],
packages=find_packages(),
zip_safe=False
)