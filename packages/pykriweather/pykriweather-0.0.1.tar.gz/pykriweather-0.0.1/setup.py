
from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(name='pykriweather',
      version='0.0.1',
      description='Python Distribution Utilities',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Krishna Mishra',
      author_email='krishna1994.m@gmail.com',
      url='https://github.com/pykrishna/pykriweather.git',
      packages=['pykriweather'],
      license='MIT',
      install_requires=['pyowm']
     )