from setuptools import setup, find_packages

setup(name="seqreppy",
      version="1.0.2",
      description="Python library for numerical representations of genomic sequences",
      long_description=open("README.txt").read() + "\n\n",
      url="https://github.com/ednilsonlomazi/seqreppy",
      author="Ednilson Lomazi",
      author_email="ednilson.lomazi.gt@gmail.com",
      license="BSD 3-Clause License",
      packages=find_packages(),
)
