PM6-ML ASE calculator
=====================

This package provides [Atomic Simulation Environment (ASE)](https://wiki.fysik.dtu.dk/ase/index.html) calculator implementing [PM6-ML](https://pubs.acs.org/doi/10.1021/acs.jctc.4c01330), a Δ-ML method combining PM6 semiempirical quantum-chemical calulation with a machine learning correction.

**The model file containing the ML parameters

- [ ] Add license
- [ ] Experiment with the dependencies
- [ ] Write better readme
- [ ]
- [ ]
- [ ]

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
conda install pytest
```

Install the calculator
```
pip install .
```

Testing
-------

Prior to running the tests, an environment variable `PM6ML_MODEL` must be set, pointing to the model checkpoint file for the PM6-ML correction. Then the tests can be then run with:

```
pytest
```

License
-------

The pm6ml package is licensed under LGPLv2.1 or later, the same license as ASE.
