from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 2'
]
 
setup(
  name='MayReader',
  version='0.0.1',
  description='Reader for maya ascii files',
  long_description=open('README.md').read(),
  url='',  
  author='Milan Mitrovic',
  author_email='milan.mitrovic2111@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Reader', 
  packages=find_packages(),
  install_requires=[''] 
)