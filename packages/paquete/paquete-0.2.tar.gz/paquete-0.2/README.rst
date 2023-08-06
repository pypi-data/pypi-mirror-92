Source
------
https://python-packaging.readthedocs.io/en/latest/minimal.html

Packaging
---------
Code:
package/
    module/
        __init__.py
        module_1.py
        module_2.py
    setup.py

Create Package
$ python setup.py sdist

Upload to PyPi
$ twine upload dist/paquete-0.1.tar.gz 

Install
-------
From a virtual environment:
pip install paquete

Use
---
To use it, just do::

    >> import paquete.operaciones as ops
    >> ops.suma(4,5)