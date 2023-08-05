from setuptools import setup, find_packages
 

 
setup(
  name='functions_for_mash_objects1',
  version='0.0.2',
  description='Functions for parsing of maya ascii files that returns name, position and uid of all mesh objects',
  long_description=open('README.txt').read(),
  url='',  
  author='Katarina Knezevic',
  author_email='kvknezevic@gmial.com',
  license='MIT', 
  packages=find_packages(exclude=['tests']),
  install_requires=[''] 
)
