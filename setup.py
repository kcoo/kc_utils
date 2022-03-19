# -*- coding: utf-8 -*-
import os
import pkg_resources
from setuptools import setup, find_packages

requirements = pkg_resources.resource_string(__name__, "requirements.txt")
requires = requirements.decode().split(os.linesep)

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='kc_utils',

      version="0.0.2",

      url='https://github.com/kcoo/kc_utils',

      author='yc.fqiyou',

      author_email='yc.fqiyou@gmail.com',

      description=u'kc_utils',

      install_requires=requires,

      extras_require={
            "cache_redis": [
                  'redis>=4.1.0',
            ]
      },

      packages=find_packages(),

      # long_description=open('README.md').read(),

      # long_description=long_description,

      # long_description_content_type="text/markdown",

      package_data={
      },
      entry_points={
      }

)



# source activate yc_python3.6_dev
# python setup.py sdist
# python setup.py install
# pip install --upgrade kc_utils -i https://pypi.org/simple/
# pip install --upgrade kc_utils['cache_redis'] -i https://pypi.org/simple/


# /usr/local/app/minionda/miniconda2/envs/yc_python3.6_dev/bin/python  setup.py bdist_wheel upload