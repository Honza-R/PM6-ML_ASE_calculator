#!/usr/bin/env python3

import os
import pytest
import ase.io
import ase.units
from pm6ml import PM6MLCalculator


def test_interaction_energy():
    # Load water dimer
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wd.xyz")
    atoms = ase.io.read(fn, format="xyz", index=":")[0]
    atoms.info.update({"charge": 0, "spin": 1})
    # Select the monomers
    atoms_a = atoms[[0, 1, 2]]
    atoms_a.info.update({"charge": 0, "spin": 1})
    atoms_b = atoms[[3, 4, 5]]
    atoms_b.info.update({"charge": 0, "spin": 1})
    # Set up calculations
    atoms.calc = PM6MLCalculator()
    atoms_a.calc = PM6MLCalculator()
    atoms_b.calc = PM6MLCalculator()
    # Run calculations
    energy = atoms.get_potential_energy() / ase.units.kcal * ase.units.mol
    energy_a = atoms_a.get_potential_energy() / ase.units.kcal * ase.units.mol
    energy_b = atoms_b.get_potential_energy() / ase.units.kcal * ase.units.mol
    # Get interaction energy
    e_int = energy - energy_a - energy_b
    assert abs(e_int - -4.9) < 0.1


if __name__ == "__main__":
    pytest.main()
