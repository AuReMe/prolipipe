.. image:: https://img.shields.io/github/license/AuReMe/metage2metabo.svg
	:target: https://github.com/NoeRobert1/prolipipe-1/blob/main/LICENSE


Prolipipe : large-scale assessment of metabolic profiles focusing on specific pathways.
===================================================================================================

Assessing capacity to synthesize or degrade specific compounds among a large set of metabolic networks and screen them accordingly.

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

Prolipipe relies on outputs from the `"AuFAMe" package <https://github.com/AuReMe/MeReco>`__
It runs with python >= 3.8.

These python packages are needed :

    - `pandas <https://pandas.pydata.org/>`__
    - `numpy <https://numpy.org/>`__
    - `plotly <https://plotly.com/>`__
    - glob2
    - jupyter
    - papermill
    - `padmet <https://github.com/AuReMe/padmet>`__

Prolipipe also needs `Quarto <https://quarto.org/>`__ to generate the interactive report (version > 1.7). 

Conda
~~~~

Prolipipe is available on the conda channel "fermentsdufutur" and can be installed with:

.. code:: sh

	conda create -n prolipipe
	conda activate prolipipe
	conda install -c fermentsdufutur prolipipe 

Preparation of taxfile
-----

Prolipipe and AuFAMe rely on data about genomes, either a taxonomic ID for building accurate GSMs in the case of AuFAMe or species name and assembly level categories for clustering during Prolipipe's analyses.
A compatible structure for both is the following columns in a tsv file :

    - "Species" : space-separated species name (used to categorize genomes in reports and heatmaps)
    - "Taxon_id" : strict taxID of the species ; can be "2" (Bacteria) if ignored
    - "Filename" : strict name of the genome file, without file extension
    - "Strain" : space-separated strain name
    - "Status" : another metric to categorize genomes based on assembly quality ; that way, can be either "Complete", "Chromosome", "Scaffold" and "Contig"

Preparation of pathways 
-----
You need to prepare a "pathways" directory before running Prolipipe. To do so, gather pathways of interest for your study from `MetaCyc <https://metacyc.org/>`__ and build pathway-specific txt files made of the reactions identifiers composing it, one per line. 
An exemple of pathways directory is given in "toy_example/pathways". 

Usage
-----
To run Prolipipe with padmet files from AuFAMe as input, generate TSV files and an interactive Quarto report:

.. code:: python

	prolipipe -pad DIRECTORY --tax TAXFILE --pwy PWY_FOLD

To generate TSV files without the Quarto report:

.. code:: python

    prolipipe -pad DIRECTORY --tax TAXFILE --pwy PWY_FOLD --no-report
    
To run Prolipipe with TSV files from AuFAMe as input and generate an interactive Quarto report:

.. code:: python

    prolipipe -i DIRECTORY --tax TAXFILE --pwy PWY_FOLD

To regenerate Quarto report from TSV files created by Prolipipe:

.. code:: python

	prolipipe-report -i DIRECTORY -d OUT_DIRECTORY 

