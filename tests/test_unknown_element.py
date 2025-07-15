#!/usr/bin/env python3

import os
import pytest
import ase.io
from ase.calculators.fd import FiniteDifferenceCalculator
from pm6ml import PM6MLCalculator


def test_unknown_element():
    # Load xyz file with element W
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unknown_element.xyz")
    atoms = ase.io.read(fn, format="xyz", index=":")[0]
    # Calculator - no model provided, environment variable PM6ML_MODEL must be set
    atoms.calc = PM6MLCalculator()
    # Calculate
    with pytest.raises(RuntimeError):
        energy = atoms.get_potential_energy()

if __name__ == "__main__":
    pytest.main()
