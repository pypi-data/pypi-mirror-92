import logging

from setuptools import setup

from niftypet.ninst import cudasetup as cs
from niftypet.ninst import install_tools as tls

logging.basicConfig(level=logging.INFO, format=tls.LOG_FORMAT)


tls.check_platform()
ext = tls.check_depends()  # external dependencies

# install resources.py
if ext["cuda"] and ext["cmake"]:
    # select the supported GPU device and
    gpuarch = cs.resources_setup()
else:
    gpuarch = cs.resources_setup(gpu=False)

setup(use_scm_version=True)
