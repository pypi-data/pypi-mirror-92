#from distutils.core import setup, Extension
from setuptools import setup, Extension
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

os.environ["CC"] = "gcc-10.2"
os.environ['CFLAGS'] = '-O3 -fopenmp -pthread'
setup(name="doryrips",
      version="0.0.2",
      description="Python interface for the Dory",
      author="Manu Aggarwal",
      author_email="manu.aggarwal@nih.gov",
      ext_modules=[Extension("doryrips", ["dorymodule.c"])]
      #extra_compile_args = ["-O3 -fopenmp -pthread"], 
      )
