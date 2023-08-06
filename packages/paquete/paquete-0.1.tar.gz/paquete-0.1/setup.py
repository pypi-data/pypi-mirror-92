# https://python-packaging.readthedocs.io/en/latest/minimal.html
from setuptools import setup


def readme():
      with open("README.rst") as f:
            return f.read()


setup(name="paquete",
      version="0.1",
      description="paquete de operaciones",
      long_description="kepa queton",
      classifiers=["Development Status :: 1 - Planning",
                   "License :: OSI Approved :: GNU General Public License (GPL)",
                   "Programming Language :: Python :: 3.7"],
      keywords="algebra operation",
      url="https://gitlab.com/personal39/paquete.git",
      author="dbp",
      author_email="dbp@ugr.es",
      license="UGR",
      packages=["paquete"],
      install_requires=["numpy"],
      include_package_data=True,
      zip_safe=False,
      test_suite="nose.collector",
      test_require=['nose'],
      )
