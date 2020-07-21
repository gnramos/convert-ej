from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="convert-ej",
    version="1.1.6",
    description="A software tool for converting problem files between electronic judges formats.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/gnramos/convert-ej",
    author="Tiago de Souza Fernandes",
    author_email="tiagotsf2000@gmail.com",
    license="GNU GENERAL PUBLIC LICENSE",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["convert_ej"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "convert-ej=convert_ej.convert:main",
        ]
    },
)
