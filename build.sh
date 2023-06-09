#!/bin/bash
pip uninstall clenv
python setup.py sdist bdist_wheel
pip install -e .
# twine upload dist/*