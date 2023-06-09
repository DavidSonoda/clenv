from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="clenv",
    version="0.0.6",
    description="ClearML config profile manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Juewei Dong",
    author_email="juewei.dong@brainco.tech",
    url="https://github.com/DavidSonoda/clenv",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "clenv = clenv.cli.__main__:main",
        ],
    },
    install_requires=[
        "clearml>=1.10.0",
        "click>=8.1.0",
        "pyhocon==0.3.35",
        "bcrypt>=4.0.0",
    ],
)
