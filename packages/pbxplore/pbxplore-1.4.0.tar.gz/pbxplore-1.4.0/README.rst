PBxplore
========

.. image:: https://img.shields.io/badge/Python-3.6%203.8-brightgreen.svg
    :alt: Python version
    :target: https://pypi.python.org/pypi/pbxplore

.. image:: https://badge.fury.io/py/pbxplore.svg
    :alt: PyPI PBxplore version
    :target: https://pypi.python.org/pypi/pbxplore

.. image:: https://travis-ci.org/pierrepo/PBxplore.svg?branch=master
    :alt: Travis CI build status
    :target: https://travis-ci.org/pierrepo/PBxplore

.. image:: https://readthedocs.org/projects/pbxplore/badge/?version=latest
    :alt: PBxplore documentation
    :target: https://pbxplore.readthedocs.org/en/latest/


**PBxplore** is a suite of tools dedicated to Protein Block (PB) analysis.
Protein Blocks are structural prototypes defined by
`de Brevern et al <https://www.ncbi.nlm.nih.gov/pubmed/11025540>`_. The 3-dimensional local
structure of a protein backbone can be modelized as an 1-dimensional sequence of PBs.
In principle, any conformation of any amino acid could be represented by one of
the sixteen available Protein Blocks (see Figure 1).

.. image:: https://raw.githubusercontent.com/pierrepo/PBxplore/master/doc/source/img/PBs.jpg
    :alt: PBs

**Figure 1.** Schematic representation of the sixteen protein blocks,
labeled from *a* to *p* (`Creative commons 4.0 CC-BY <https://creativecommons.org/licenses/by/4.0/>`_).


PBxplore provides both a Python library and command-line tools. Basically, PBxplore can:

* **assign PBs** from a single PDB, many PDBs or a molecular dynamics simulation trajectory.
* use analysis tools to perform **statistical analysis** on PBs.
* use analysis tools to **study protein flexibility and deformability**.


Requirements
------------

PBxplore requires:

* Python 3.x (>= 3.6)
* Python modules: `NumPy <http://numpy.scipy.org/>`_, `Matplotlib <http://matplotlib.org/>`_, `MDAnalysis <https://code.google.com/p/mdanalysis/>`_ (version >= 0.11).

Optionally, PBxplore can use:

* `WebLogo 3 <http://weblogo.threeplusone.com/>`_ to create logo from PB sequences.


Installation
------------

Once dependencies installed, the most straightforward way is to use `pip`:

.. code-block:: bash

    $ pip install pbxplore


PBxplore can also be installed for the current user only:

.. code-block:: bash

    $ pip install --user pbxplore


Documentation
-------------

All documentation are hosted by Read The Docs and can be found `here <https://pbxplore.readthedocs.org/en/latest/>`_.


Citation
--------

If you use PBxplore, please cite this tool as:

| Barnoud J, Santuz H, Craveur P, Joseph AP, Jallu V, de Brevern AG, Poulain P,
| PBxplore: a tool to analyze local protein structure and deformability with Protein Blocks
| *PeerJ*  5:e4013 `<https://doi.org/10.7717/peerj.4013>`_ (2017).


Contact & Support
-----------------

PBxplore is a research software and has been developped by:

* Pierre Poulain, "Mitochondria, Metals and Oxidative Stress" group, Institut Jacques Monod, UMR 7592, Univ. Paris, CNRS, France.
* Jonathan Barnoud, University of Groningen, Groningen, The Netherlands.
* Hubert Santuz, Laboratoire de Biochimie Théorique, CNRS UPR 9080, Institut de Biologie Physico-Chimique, Paris, France.
* Alexandre G. de Brevern & Gabriel Cretin, DSIMB, INSERM, UMR_S 1134, INTS, Univ Paris, Paris, France.

If you want to report a bug, request a feature,
use the `GitHub issue system <https://github.com/pierrepo/PBxplore/issues>`_.


License
-------

PBxplore is licensed under `The MIT License <https://github.com/pierrepo/PBxplore/blob/master/LICENSE>`_.

