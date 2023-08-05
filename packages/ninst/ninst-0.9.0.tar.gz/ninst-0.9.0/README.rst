==================================
NInst: NiftyPET Installation Tools
==================================

|Docs| |Version| |Py-Versions| |Tests| |Coverage|

``ninst`` is a stand-alone Python sub-package of NiftyPET_, dedicated to helping with installation of other sub-packages. Although it is an essential part of NiftyPET_ packaging, ``ninst`` could be used in other projects.

.. _NiftyPET: https://github.com/NiftyPET/NiftyPET

**Documentation with installation manual and tutorials**: https://niftypet.readthedocs.io/

Install
~~~~~~~

.. code:: sh

    pip install ninst

Note that installation prompts for setting the path to ``NiftyPET_tools``.
This can be avoided by setting the environment variables ``PATHTOOLS``.
It's also recommended (but not required) to use `conda`.

.. code:: sh

    # optional (Linux syntax) to avoid prompts
    export PATHTOOLS=$HOME/NiftyPET_tools
    # cross-platform install
    conda install -c conda-forge python=3
    pip install ninst

Licence
~~~~~~~

|Licence|

Copyright 2018-21

- `Casper O. da Costa-Luis <https://github.com/casperdcl>`__ @ King's College London
- `Pawel J. Markiewicz <https://github.com/pjmark>`__ @ University College London
- `Contributors <https://github.com/NiftyPET/NInst/graphs/contributors>`__

.. |Docs| image:: https://readthedocs.org/projects/niftypet/badge/?version=latest
   :target: https://niftypet.readthedocs.io/en/latest/?badge=latest
.. |Licence| image:: https://img.shields.io/pypi/l/ninst.svg?label=licence
   :target: https://raw.githubusercontent.com/NiftyPET/NInst/master/LICENCE
.. |Tests| image:: https://img.shields.io/github/workflow/status/NiftyPET/NInst/Test?logo=GitHub
   :target: https://github.com/NiftyPET/NInst/actions
.. |Coverage| image:: https://codecov.io/gh/NiftyPET/NInst/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/NiftyPET/NInst
.. |Version| image:: https://img.shields.io/pypi/v/ninst.svg?logo=python&logoColor=white
   :target: https://github.com/NiftyPET/NInst/releases
.. |Py-Versions| image:: https://img.shields.io/pypi/pyversions/ninst.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ninst
