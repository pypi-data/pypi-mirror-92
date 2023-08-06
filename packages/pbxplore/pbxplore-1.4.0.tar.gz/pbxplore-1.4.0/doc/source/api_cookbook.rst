API Cookbook
============

This page provides some examples, tutorials as notebooks to help you use the API of ``PBxplore``.

Basically, PBxplore is structured around 3 modules:

PBxplore.structure
------------------

This module handles the reading of PDB files and trajectory files.
Its 2 major functions `chain_from_files()` and `chain_from_trajectory` are direclty exposed
at the package level.

Look at the notebook  :doc:`PB assignation <./notebooks/Assignement>` for further information.


PBxplore.io
-----------

This module is about the I/O of all files other than PDB.
It handles the reading/writing of fasta files and the writing of
text-like analysis files (Neq files).

Look at the notebook  :doc:`Writing PB in file <./notebooks/WritePB>` for further information.


PBxplore.analysis
-----------------

This module handle all analysis functions and ploting functions.
You can:

* generate map of the distribution of PBs along protein sequence with `plot_map()`.
* compute :ref:`Neq` with `compute_neq()` and generate the plot with `plot_neq()`.
* generate WebLogo-like representation of PBs frequency along protein sequence with `generate_weblogo()`.

Look at the notebook :doc:`Visualize protein deformability <./notebooks/Deformability>`
for further information.


.. note:: `generate_weblogo()` requires `Weblogo3 <http://weblogo.threeplusone.com/>`_.


.. toctree::
   :maxdepth: 1

   ./notebooks/Assignement
   ./notebooks/WritePB
   ./notebooks/Deformability
