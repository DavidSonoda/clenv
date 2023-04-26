#!/bin/bash
python setup.py sdist bdist_wheel
# pip install -e .
# twine upload dist/*