.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - \1. Code repository
     - |GitHub Badge|
   * - \2. License
     - |License Badge|
   * - Continuous integration
     - |Python Build| |PyPI Publish|
   * - Code Coverage
     - |Coveralls|

(Customize these badges with your own links, and check https://shields.io/ or https://badgen.net/ to see which other badges are available.)

.. |GitHub Badge| image:: https://img.shields.io/badge/github-repo-000.svg?logo=github&labelColor=gray&color=blue
   :target: https://github.com/NLeSC/vantage6-algorithms
   :alt: GitHub Badge

.. |License Badge| image:: https://img.shields.io/github/license/CARRIER-project/vantage6-algorithms
   :target: https://github.com/NLeSC/vantage6-algorithms
   :alt: License Badge

.. |PyPI Badge| image:: https://img.shields.io/pypi/v/vantage6-algorithms.svg?colorB=blue
   :target: https://pypi.python.org/project/vantage6-algorithms/
   :alt: PyPI Badge
.. |Research Software Directory Badge| image:: https://img.shields.io/badge/rsd-vantage6-algorithms-00a3e3.svg
   :target: https://www.research-software.nl/software/vantage6-algorithms
   :alt: Research Software Directory Badge

..
    Goto https://zenodo.org/account/settings/github/ to enable Zenodo/GitHub integration.
    After creation of a GitHub release at https://github.com/NLeSC/vantage6-algorithms/releases
    there will be a Zenodo upload created at https://zenodo.org/deposit with a DOI, this DOI can be put in the Zenodo badge urls.
    In the README, we prefer to use the concept DOI over versioned DOI, see https://help.zenodo.org/#versioning.
.. |Zenodo Badge| image:: https://zenodo.org/badge/DOI/< replace with created DOI >.svg
   :target: https://doi.org/<replace with created DOI>
   :alt: Zenodo Badge

..
    A CII Best Practices project can be created at https://bestpractices.coreinfrastructure.org/en/projects/new
.. |CII Best Practices Badge| image:: https://bestpractices.coreinfrastructure.org/projects/< replace with created project identifier >/badge
   :target: https://bestpractices.coreinfrastructure.org/projects/< replace with created project identifier >
   :alt: CII Best Practices Badge

.. |Python Build| image:: https://img.shields.io/github/workflow/status/CARRIER-project/vantage6-algorithms/Build
   :alt: Python Build

.. |PyPI Publish| image:: https://github.com/NLeSC/vantage6-algorithms/workflows/PyPI/badge.svg
   :target: https://github.com/NLeSC/vantage6-algorithms/actions?query=workflow%3A%22PyPI%22
   :alt: PyPI Publish
   
.. |Coveralls| image:: https://coveralls.io/repos/github/CARRIER-project/vantage6-algorithms/badge.svg?branch=master
   :target: https://coveralls.io/github/CARRIER-project/vantage6-algorithms?branch=master


*******************
vantage6-algorithms
*******************

Algorithms developed for running on Vantage6


Installation
############

To install vantage6-algorithms, do:

.. code-block:: console

  git clone https://github.com/NLeSC/vantage6-algorithms.git
  cd vantage6-algorithms
  pip install .


Run tests (including coverage) with:

.. code-block:: console

  python setup.py test


Algorithms
##########
The algorithms in this repo ar part of the vantage6_ solution. Vantage6 allows to execute computations on federated 
datasets. 

.. _vantage6: https://vantage6.ai

TODO: Table with instructions how to call the different algorithms

Analysis of Vertically Partitioned Data Using a TSE
***************************************************


Based on the implementation of [SOEST2020]_

.. [SOEST2020] van Soest PhD, Johan, Sun MSc, Chang, & Mussmann PhD, Bjoern Ole. (2020, February 4). FAIRHealth (Version v0.0.5). Zenodo. http://doi.org/10.5281/zenodo.3635839

Workarounds
###########
As the vantage6 software is still in heavy development we sometimes have to create workarounds to get the package to 
work correctly. 

Vantage-6 dependencies
**********************
At time of writing, the algorithms implemented in this repository are not yet compatible with the vantage6 packages
from pypi. That is why `requirements.txt` refers to branch `1.1.0` in the github repos of the vantage6 packages.
When all required changes are pushed to pypi these depencencies will have to be replaced with pypi dependencies.

Read More
#########
See the `vantage6 documentation`__ for detailed instructions on how to install and use the server and nodes.

.. __: https://docs.vantage6.ai/

Contributing
############

If you want to contribute to the development of vantage6-algorithms,
have a look at the `contribution guidelines <CONTRIBUTING.rst>`_.

License
#######
Copyright 2020

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Credits
#######

This package was created with `Cookiecutter <https://github.com/audreyr/cookiecutter>`_ and the `NLeSC/python-template <https://github.com/NLeSC/python-template>`_.
