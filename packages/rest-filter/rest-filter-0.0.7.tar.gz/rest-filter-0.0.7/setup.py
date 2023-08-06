import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = os.getenv('REST_FILTER_VERSION', '0.0.6')

setuptools.setup(
    name="rest-filter",
    version=version,
    author="Sagiv Oulu",
    author_email="sagiv.oulu@gmail.com",
    description="A query string parsing library for REST server queries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/sagbot/odata_parser",
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
