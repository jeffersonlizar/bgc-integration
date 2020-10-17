from distutils.core import setup

import setuptools

setup(
    name="bgc_integrations",
    version="0.4dev",
    packages=setuptools.find_packages(),
    license="",
    long_description=open("README.md").read(),
    install_requires=[
        "Flask==1.1.2",
        "redis==3.5.3",
        "pytest==6.1.1",
        "python-redis-lock==3.6.0",
        "requests==2.21.0",
        "six==1.15.0",
        "Flask-Caching==1.8",
    ],
)
