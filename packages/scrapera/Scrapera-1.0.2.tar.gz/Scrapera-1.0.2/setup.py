from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="Scrapera",
    version="1.0.2",
    description="All in one scraping library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DarshanDeshpande/Scrapera",
    author="Darshan Deshpande",
    author_email="darshan1504@gmail.com",
    license="MIT",
    python_requires=">=3.6.0",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["scrapera"],
    include_package_data=True,
    install_requires=required,
)
