.. image:: https://img.shields.io/github/license/AuReMe/metage2metabo.svg
	:target: https://github.com/NoeRobert1/prolipipe-1/blob/main/LICENSE


Prolipipe : large-scale assessment of metabolic profiles on bacteria focusing on specific pathways.
===================================================================================================

Workflow to reconstruct multiple metabolic graphs and assess capacity to synthesize specific compounds.

.. contents:: Table of contents
   :backlinks: top
   :local:

License
--------
This workflow is licensed under the GNU GPL-3.0-or-later, see the `LICENSE <https://github.com/AuReMe/prolipipe/blob/main/LICENSE>`__ file for details.

Installation
------------

Dependencies
~~~~~~~~~~~~

Prolipipe relies on outputs from the `"MeReco" package <https://github.com/AuReMe/MeReco>`__
It runs with python >= 3.8.

These python packages are needed :

    - `pandas <https://pandas.pydata.org/>`__
    - `numpy <https://numpy.org/>`__
    - `plotly <https://plotly.com/>`__
    - glob2
    - jupyter
    - papermill

Prolipipe also needs `Quarto <https://quarto.org/>`__ to generate the interactive report (version > 1.7). 

conda
~~~~

Prolipipe is available on the conda channel "fermentsdufutur" and can be installed with:

.. code:: sh

	conda create -n prolipipe
	conda activate prolipipe
	conda install -c fermentsdufutur prolipipe 

Usage
-----
To run Prolipipe and generate an interactive Quarto report:

.. code:: python

    prolipipe [-h] -d DIRECTORY --tax TAXFILE --pwy PWY_FOLD

To generate TSV files without the Quarto report:

.. code:: python

    prolipipe [-h] -d DIRECTORY --tax TAXFILE --pwy PWY_FOLD --no-report


