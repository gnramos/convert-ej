from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="EJ-Bridge",
    version="1.1.1",
    description="A Python package to translate questions \
                 between electronic judges",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/gnramos/ejtranslator",
    author="Tiago de Souza Fernandes",
    author_email="tiagotsf2000@gmail.com",
    license="GNU GENERAL PUBLIC LICENSE",
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        "Programming Language :: Python :: 3.7",
    ],
    packages=["ej_bridge"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ejbridge=ej_bridge.ejb:main",
        ]
    },
)
