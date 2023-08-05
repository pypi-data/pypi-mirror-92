from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 2'
]
 
setup(
  name='functions_for_mash_objects',
  version='0.0.1',
  description='Functions for parsing of maya ascii files that returns name, position and uid of all mesh objects',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Katarina Knezevic',
  author_email='kvknezevic@gmial.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='maya ascii', 
  packages=find_packages(),
  install_requires=[''] 
)