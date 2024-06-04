import os
import io
from setuptools import setup, find_packages
from rgbpp import __version__

HERE = os.path.dirname(os.path.realpath(__file__))

README = os.path.join(HERE, 'README.md')
with io.open(README, encoding='utf-8') as f:
    long_description = f.read()

VERSION = os.path.join(HERE, 'ckb', 'version.py')
with io.open(VERSION, encoding='utf-8') as f:
    package = {}
    exec(f.read(), package)
    version = package['VERSION']

setup(name='rgbpp-sdk-python',
      version=version,
      description='RGB++ SDK',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ckb-cell/rgbpp-sdk-python',
      author='Dylan',
      author_email='duanyytop@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['jsonrpcclient', 'requests', 'typing-extensions'],
      zip_safe=False,
      include_package_data=True,
      )