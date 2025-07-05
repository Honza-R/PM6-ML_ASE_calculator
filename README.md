PM6-ML ASE calculator
=====================

This package provides an [Atomic Simulation Environment (ASE)](https://wiki.fysik.dtu.dk/ase/index.html) calculator that implements the [PM6-ML](https://pubs.acs.org/doi/10.1021/acs.jctc.4c01330) method, which combines a PM6 semiempirical quantum-chemical calculation with a machine learning correction. 

**The model file containing the parameters for the ML correction must be installed separately** and is available as part of the [MOPAC-ML repository](https://github.com/Honza-R/mopac-ml). The path to the model file must be provided in the code or via an environment variable. See the ML Correction Models section below.

There are also other ways to run PM6-ML calculations. [MOPAC-ML](https://github.com/Honza-R/mopac-ml) is a wrapper that applies the corrections to any MOPAC calculation. The [Cuby framework](http://cuby4.molecular.cz/interface_torchmdnet.html) provides a modular implementation for the [automated processing of benchmark datasets](https://doi.org/10.1063/5.0203372) and more. PM6-ML is also available in the [pDynamo3](https://github.com/pdynamo/pDynamo3) package, which focuses on QM/MM MD simulations.

Installation
------------

The PM6-ML calculator uses the PM6 implementation in MOPAC, the D3 dispersion correction, and the TorchMD-NET ML potential. The MOPAC executable, named `mopac`, must be available in the search path. All the dependencies, including the MOPAC binary, can be installed using conda (preferably in a clean environment):
```
conda install -c conda-forge ase mopac simple-dftd3 dftd3-python torchmd-net pytest
```

The PM6-ML calculator is then installed by running the following command in the root of this repository:

```
pip install .
```

ML Correction Models
--------------------

The parameters for the ML correction used in the PM6-ML, the model checkpoint file, are provided separately in the [MOPAC-ML repository](https://github.com/Honza-R/mopac-ml) and are licensed under the Academic Software License provided therein. To use the PM6-ML calculator, download at least the default model, `PM6-ML_correction_seed8_best.ckpt`, from there.

The path to the model file must be provided to the calculator. One option is to hardcode the path in the calculator's initialization, e.g., as

```
atoms.calc = PM6MLCalculator(model_file="your_path_to/PM6-ML_correction_seed8_best.ckpt")
```

A more portable option is to set the path to the model in the environment variable `PM6ML_MODEL`, for example using `export PM6ML_MODEL=your_path_to/PM6-ML_correction_seed8_best.ckpt` in bash. Then,  the calculator can be initialized without any arguments:

```
atoms.calc = PM6MLCalculator()
```

Example
-------

The following Python code would run a simple calculation on a water molecule, assuming the `PM6ML_MODEL` environment variable is configured:

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

Before running the tests, set the environment variable `PM6ML_MODEL` to point to the PM6-ML correction model checkpoint file. Then, run the tests with:

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
