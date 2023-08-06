from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='numbercalculator',
  version='0.0.1',
  description='To calculate numbers',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Chayan Mitra',
  author_email='vectorchayanmitra@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='numbercalculator', 
  packages=find_packages(),
  install_requires=[''] 
)