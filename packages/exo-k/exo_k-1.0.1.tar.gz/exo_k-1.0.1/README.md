# Exo_k

Author: Jeremy Leconte (CNRS/LAB/Univ. Bordeaux)

`Exo_k` is a Python 3 based library to handle radiative opacities from various sources for atmospheric applications.
It enables you to:

* Interpolate efficiently and easily in correlated-k and cross section tables.
* Convert easily correlated-k and cross section tables from one format to another
  (hdf5, LMDZ GCM, Exomol, Nemesis, PetitCode, TauREx, ExoREM, ARCIS, etc.).
* Adapt precomputed correlated-k tables to your needs by changing:

  * the resolution and quadrature (g) grid,
  * the pressure/temperature grid.
* Create tables for a mix of gases using tables for individual gases.
* Create your own tables from high-resolution spectra (for example from K-spectrum, Helios-K, etc.).
* Use your data in an integrated radiative transfer framework to simulate planetary atmospheres.
  
In this repository, you'll find a [tutorial jupyter notebook](https://forge.oasu.u-bordeaux.fr/jleconte/exo_k-public/-/blob/public/tutorial-exo_k.ipynb) that will show you how to do all that
with concrete examples that you can run on your own machine. Many important concepts and options are
presented along the way.

Enjoy!

J. Leconte

# Recent releases

v1.0.1 (Jan 2021): Solves a binary/string conversion issue on some platforms.
Enables linear interpolation in pressure (default is log). Enables creation of
empty tables to filled later and spectral extension of existing tables. 

v1.0.0 (Dec 2020): Finally our first official version. Creation of a
'examples' notebook with fully worked out use cases for the `Exo_k`. 

v0.0.5 (Oct 2020): Ensures compatibility with latest Exomol correlated-k and cross-section tables.

# Installation

Exo_k can be installed using pip (without cloning the repository;
dependencies should be downloaded automatically):
```
pip install exo_k
```
Or by running the [setup.py](https://forge.oasu.u-bordeaux.fr/jleconte/exo_k-public/-/blob/public/setup.py) script in the cloned repository:
```
python setup.py install
```
# Usage

To learn how to use `exo_k`, you can follow the [tutorial jupyter notebook](https://forge.oasu.u-bordeaux.fr/jleconte/exo_k-public/-/blob/public/tutorial-exo_k.ipynb).

Have fun!

# Links

* Project homepage: http://perso.astrophy.u-bordeaux.fr/~jleconte/
* Code repository: https://forge.oasu.u-bordeaux.fr/jleconte/exo_k-public
* Documentation: http://perso.astrophy.u-bordeaux.fr/~jleconte/exo_k-doc/index.html
* Contact: jeremy.leconte at u-bordeaux.fr

# Acknowledgements

This project has received funding from the European Research Council (ERC)
under the European Union's Horizon 2020 research and innovation programme
(grant agreement n° 679030/WHIPLASH).

The framework for this documentation has been developped by Aurelien Falco using Sphinx. 

# Building the documentation

To generate the documentation, you will need to install the following packages:
```
pip install nbsphinx sphinx-autoapi sphinx_rtd_theme
conda install sphinx # installs more (required) dependencies than pip
```
You can then generate the documentation by running:
```
python setup.py doc
```
(or by simply running `make` in the `doc/` folder). The documentation will be generated in the doc/html folder (you can open the doc/html/index.html file to check it out).

