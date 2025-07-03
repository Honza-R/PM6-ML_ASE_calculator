#!/usr/bin/env python3

import ase.io
import ase.units
from pm6ml import PM6MLCalculator

atoms = ase.io.read("wd.xyz", format="xyz", index=":")[0]
atoms.info.update({"charge": 0, "spin": 1})

atoms_a = atoms[[0, 1, 2]]
atoms_a.info.update({"charge": 0, "spin": 1})

atoms_b = atoms[[3, 4, 5]]
atoms_b.info.update({"charge": 0, "spin": 1})

# Assign the calculator
model_ckpt = (
    "/home/rezac/Github/PUBLIC/mopac-ml/models/PM6-ML_correction_seed8_best.ckpt"
)
atoms.calc = PM6MLCalculator(model_ckpt)
atoms_a.calc = PM6MLCalculator(model_ckpt)
atoms_b.calc = PM6MLCalculator(model_ckpt)

energy = atoms.get_potential_energy() / ase.units.kcal * ase.units.mol
energy_a = atoms_a.get_potential_energy() / ase.units.kcal * ase.units.mol
energy_b = atoms_b.get_potential_energy() / ase.units.kcal * ase.units.mol
print(energy - energy_a - energy_b)
