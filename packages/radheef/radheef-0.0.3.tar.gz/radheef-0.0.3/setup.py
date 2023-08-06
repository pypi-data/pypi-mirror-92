# author : Moots (github.com/mootss)
# setup file for radheef.py

from setuptools import setup, find_packages

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("README.md", encoding="utf8") as f:
    global readme
    readme = f.read()

version = "0.0.3" 
desc = "A python library for getting the meaning/s of a dhivehi word and other related information"

setup(
        name="radheef", 
        version=version,
        author="Moots",
        author_email="moothymycom@gmail.com",
        description=desc,
        long_description=readme,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=requirements,
        license='MIT License',
        
        keywords=['radheef', 'dhivehi dictionary'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            "License :: OSI Approved :: MIT License"
        ]
)

# last updated: 22/02/2021