#!/usr/bin/env python3

import ase.io
from ase.calculators.fd import FiniteDifferenceCalculator
from pm6ml import TorchMDNetCalculator

atoms = ase.io.read("wd.xyz", format="xyz", index=":")[0]

model_ckpt = "/home/rezac/Github/PUBLIC/mopac-ml/models/PM6-ML_correction_seed8_best.ckpt"

# Gradient test
# Print analytical forces:
print("Analytical forces")
atoms.calc = TorchMDNetCalculator(model_ckpt)
forces_a = atoms.get_forces()
print(forces_a)
# Print numerical forces
print("Numerical forces")
forces_n = ase.calculators.fd.calculate_numerical_forces(atoms, eps=1.0e-3)
print(forces_n)
# Difference
print("Difference")
print(forces_a - forces_n)
