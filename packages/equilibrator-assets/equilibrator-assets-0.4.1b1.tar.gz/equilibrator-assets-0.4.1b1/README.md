eQuilibrator Assets
===================

[![pipeline status](https://gitlab.com/equilibrator/equilibrator-assets/badges/master/pipeline.svg)](https://gitlab.com/equilibrator/equilibrator-assets)
[![codecov](https://codecov.io/gl/equilibrator/equilibrator-assets/branch/master/graph/badge.svg)](https://codecov.io/gl/equilibrator/equilibrator-assets)
[![Join the chat at https://gitter.im/equilibrator-devs/equilibrator-api](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/equilibrator-devs/equilibrator-api?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A database application for caching data used by eQuilibrator and related projects.
Stored data includes compound names, structures, protonation state information,
reaction and enzyme info, and cross-references to other databases.
The majority of compounds stored in equilibrator-assets are cross-referenced
using
[InChIKey](https://en.wikipedia.org/wiki/International_Chemical_Identifier#InChIKey).

Supported Chemical Databases:
=============================

* [MetaNetX](https://www.metanetx.org/)
* [KEGG](https://www.kegg.jp/)
* [ChEBI](https://www.ebi.ac.uk/chebi/)

Installation:
=============

Some scripts in `equilibrator-assets` depend on [OpenBabel](http://openbabel.org/wiki/Main_Page), which currently cannot be installed using `pip`. We recommend installing it via `conda` instead. First, make sure you have conda or miniconda on your system. Then run this in the terminal:
```bash
conda create --name eq_assets python=3.7
source activate eq_assets
conda install -c conda-forge openbabel
pip install -e .
```

In addition, you'll need to install [Marvin (by ChemAxon)](https://chemaxon.com/products/marvin),
which requires a license. Make sure that the command `cxcalc` is
in the shell path as it is called directly using `subprocess.run()`.
