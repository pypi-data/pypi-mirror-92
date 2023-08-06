from setuptools import setup, Extension, find_packages
import re

def find_version(fname):
    with open(fname,'r') as file:
        version_file=file.read()
        version_match = re.search(r"__VERSION__ = ['\"]([^'\"]*)['\"]",version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

with open("README.md", "r") as handle:
    cytolysis_description = handle.read()

version=find_version("src/cytosim_analysis.py")

setup(
     name='cytolysis',
     version=version,



     author="Serge Dmitrieff",
     description="An API to analyze cytosim simulations",
     long_description=cytolysis_description,
     long_description_content_type='text/markdown',
     url="https://github.com/SergeDmi/Python-Tools/",
     install_requires=[
          'numpy',
          'sio_tools',
          'pandas'
      ],
     packages=find_packages(),
     scripts=['src/cytosim_analysis.py', 'src/anutils.py', 'src/read_config.py',
              'src/fibers.py', 'src/couples.py', 'src/objects.py']
 )
