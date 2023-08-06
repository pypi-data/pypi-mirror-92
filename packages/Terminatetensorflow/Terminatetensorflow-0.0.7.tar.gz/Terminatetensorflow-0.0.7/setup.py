from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Terminatetensorflow',
  version='0.0.7',
  description='A very basic NN framework',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/ASU-DEVs/NNFramework',  
  author='98Passant_Elbaroudy.98',
  author_email='passantbaroodyy@hotmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='layer', 
  packages=find_packages(),
  install_requires=[''] 
)