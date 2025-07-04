PM6-ML ASE calculator
=====================

This package provides [Atomic Simulation Environment (ASE)](https://wiki.fysik.dtu.dk/ase/index.html) calculator implementing [PM6-ML](https://pubs.acs.org/doi/10.1021/acs.jctc.4c01330), a Δ-ML method combining PM6 semiempirical quantum-chemical calulation with a machine learning correction.

**The model file containing the parameters for the ML corrections must be installed separately.** It is available as a part of the [MOPAC-ML repository](https://github.com/Honza-R/mopac-ml). The path to the model file has to be provided in the code, or via an environment variable. See the section ML Correction Models below.

Installation
------------

The PM6-ML calculator uses MOPAC, D3 dispersion and TorchMD-NET. All the dependencies can be installed using conda (preferably in a clean environment):

```
conda install -c conda-forge ase mopac simple-dftd3 dftd3-python torchmd-net pytest
```

The PM6-ML calculator is then installed by running the following command in the root of this repository:

```
pip install .
```

ML Correction Models
--------------------

The parameters for the ML correction used in PM6-ML, the model checkpoint file, are provided separately in the [MOPAC-ML repository](https://github.com/Honza-R/mopac-ml) and licensed under the Academic Software Licence provided therein. To use the PM6-ML calculator, download at least the default model, `PM6-ML_correction_seed8_best.ckpt`, from there.

The path to the model file has to be passed to the calculator. One option is to hardcode it in the initialization of the calculator, e.g. as

```
atoms.calc = PM6MLCalculator(model_file="your_path_to/PM6-ML_correction_seed8_best.ckpt")
```

A more portable option is to set the path to the model in an evironment variable `PM6ML_MODEL`, e.g. using `export PM6ML_MODEL=your_path_to/PM6-ML_correction_seed8_best.ckpt` in bash, and then initializing the model without any arguments: 

```
atoms.calc = PM6MLCalculator()
```

Example
-------

Assuming the PM6ML_MODEL environment variable is configured, the following python code would run a simple calculation on a water molecule:

```
from ase.build import molecule
from pm6ml import PM6MLCalculator

atoms = molecule('H2O')
atoms.calc = PM6MLCalculator()
energy = atoms.get_potential_energy()
print(f"Enegy of a water molecule: {energy} eV")
```

Testing
-------

Prior to running the tests, an environment variable `PM6ML_MODEL` must be set, pointing to the model checkpoint file for the PM6-ML correction. Then the tests can be then run with:

```
pytest
```

How to cite
-----------

When reporting results computed with the PM6-ML method, please cite the paper on it:<br>
Nováček M., Řezáč J., *J. Chem. Theory Comput.* **2005**, 21, 2, 678-690. [DOI: 10.1021/acs.jctc.4c01330](https://doi.org/10.1021/acs.jctc.4c01330)

License
-------

The pm6ml package is licensed under LGPLv2.1 or later, the same license as ASE.
