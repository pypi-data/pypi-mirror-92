from setuptools import setup, find_packages


classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
name='herokupackage',
version='0.1.0',
author='Yang',
author_email='yoyoo6021@hotmail.com',
url='',
license='MIT',
classifiers=classifiers,
description='heroku package',
long_description=open('README.txt').read(),
packages=find_packages(),
install_requires=["numpy==1.19.5",
"pandas==1.0.0",
"pmdarima==1.8.0",
"scikit-learn==0.24.0"]
)