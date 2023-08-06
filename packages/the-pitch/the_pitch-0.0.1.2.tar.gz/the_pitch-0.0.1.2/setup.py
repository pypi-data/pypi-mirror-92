import setuptools
from setuptools import version

setuptools.setup(
  name='the_pitch',
  version="0.0.1.2",
  description='',
  packages=setuptools.find_packages('src'),
  package_dir={'': 'src'},
  install_requires=[
    'pytest',
    'pandas',
    'numpy',
    'pandas_datareader',
    'pandas_ta',
  ]
)