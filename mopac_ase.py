#!/usr/bin/env python3

import ase.io
import ase.units

# ===============================================================================
from ase.calculators.mixing import SumCalculator
from ase.calculators.mopac import MOPAC

# D3 correction:
# Built-in ASE calculator, needs dftd3 executable:
# from ase.calculators.dftd3 import DFTD3
# DFTD3 from simple-dftd3 package:
from dftd3.ase import DFTD3


class PM6MLCalculator(SumCalculator):

    def __init__(self):
        calcs = [
            MOPAC(label="calc_mopac", method="PM6"),
            # Built-in ASE calculator, needs dftd3 executable:
            # DFTD3(damping="bj", s6=1.0, s8=0.3908, a1=0.566, a2=3.128, abc=True, alpha6=16.0)
            # DFTD3 from simple-dftd3 package:
            DFTD3(
                damping="d3bj",
                params_tweaks={
                    "s6": 1.0,
                    "s8": 0.3908,
                    "a1": 0.566,
                    "a2": 3.128,
                    "s9": 1.0,
                    "alp": 16.0,
                },
            ),
        ]
        super().__init__(calcs)


# ===============================================================================

atoms = ase.io.read("wd.xyz", format="xyz", index=":")[0]
atoms.info.update({"charge": 0, "spin": 1})

atoms_a = atoms[[0, 1, 2]]
atoms_a.info.update({"charge": 0, "spin": 1})

atoms_b = atoms[[3, 4, 5]]
atoms_b.info.update({"charge": 0, "spin": 1})

# Assign the calculator
atoms.calc = PM6MLCalculator()
atoms_a.calc = PM6MLCalculator()
atoms_b.calc = PM6MLCalculator()

energy = atoms.get_potential_energy() / ase.units.kcal * ase.units.mol
energy_a = atoms_a.get_potential_energy() / ase.units.kcal * ase.units.mol
energy_b = atoms_b.get_potential_energy() / ase.units.kcal * ase.units.mol
print(energy - energy_a - energy_b)
