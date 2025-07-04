#!/usr/bin/env python3

import os
import pytest
import ase.io
from ase.calculators.fd import FiniteDifferenceCalculator
from pm6ml import PM6MLCalculator


def test_forces():
    # Load water dimer structure
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wd.xyz")
    atoms = ase.io.read(fn, format="xyz", index=":")[0]
    # Calculator - no model provided, environment variable PM6ML_MODEL must be set
    atoms.calc = PM6MLCalculator()
    # Analytical forces
    forces_a = atoms.get_forces()
    # Numerical forces
    forces_n = ase.calculators.fd.calculate_numerical_forces(atoms, eps=1.0e-3)
    # Evaluate the difference
    difference = forces_a - forces_n
    max_diff = difference.max()
    assert max_diff < 1.0e-3


if __name__ == "__main__":
    pytest.main()
