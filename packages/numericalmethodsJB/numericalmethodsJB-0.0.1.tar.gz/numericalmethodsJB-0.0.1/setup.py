from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='numericalmethodsJB',
    version='0.0.1',
    description='A library containing numerical methods to solve problems computationally',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["rootfinding"],
    package_dir={'': 'src'},
    url="https://github.com/javierb07/numerical-methodspip install check-manifest",
    author="Javier Belmonte",
    author_email="javierbelmonte07@gmail.com", 
) 
