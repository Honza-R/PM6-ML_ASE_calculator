PM6-ML ASE calculator
=====================

Setup
-----

The PM6-ML calculator uses MOPAC, D3 dispersion and TorchMD-NET. All these can be installed using conda:

```
conda create -n PM6-ML_ASE_calculator
conda activate PM6-ML_ASE_calculator
conda install -c conda-forge ase
conda install -c conda-forge mopac
conda install -c conda-forge simple-dftd3 dftd3-python
conda install -c conda-forge torchmd-net

```
