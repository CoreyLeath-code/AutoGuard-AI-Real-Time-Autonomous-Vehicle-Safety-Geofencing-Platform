"""Legacy setuptools entry point.

Package metadata and package discovery are defined in ``pyproject.toml``. This
shim keeps older build front-ends working without importing Torch or requiring
a CUDA toolchain for the core prototype package.
"""

from setuptools import setup

if __name__ == "__main__":
    setup()
