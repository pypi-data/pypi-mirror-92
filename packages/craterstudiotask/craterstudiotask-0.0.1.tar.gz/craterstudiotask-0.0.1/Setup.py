  
from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python'
]
 
setup(
  name='craterstudiotask',
  version='0.0.1',
  description='Getting data of mesh objects from .ma example files',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  python_requires='>=2.7',
  author='Uros Jevtic',
  author_email='meksa96@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='parser', 
  packages=find_packages(),
  install_requires=[''] 
)
