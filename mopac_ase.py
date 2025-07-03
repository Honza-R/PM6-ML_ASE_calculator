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

# ===============================================================================
# TorchMDNet calculator

import numpy as np
# Torch and TorchMD-NET
import torch
from torchmdnet.models.model import load_model


from ase.calculators.calculator import Calculator, all_changes

class TorchMDNet(Calculator):

    implemented_properties = ['energy', 'forces']

    # Model - each model is loaded once
    models = {}

    def __init__(self, model_file, device=None):
        """
        Parameters
        ----------
        model_file: string
          Path to the model checkpoint file
        device: None or str
          Device used by Torch. None for default selection. "cpu" to enforce CPU.

        """
        # Parent init
        Calculator.__init__(self)

        # Load the model if not already available
        self.model_index = (model_file, device)
        if not self.model_index in TorchMDNet.models:
            print("Loading model")
            # Device to be used
            if device:
                new_device = torch.device(device)
            else:
                new_device = torch.get_default_device()
            # Load model
            new_model = load_model(model_file, derivative=True)
            new_model.to(new_device)
            TorchMDNet.models[self.model_index] = (new_model, new_device)

    def calculate(
        self,
        atoms=None,
        properties=None,
        system_changes=all_changes,
    ):

        # If no speific request is made, all properties are calculated
        if properties is None:
            properties = self.implemented_properties

        # Parent calculator call
        Calculator.calculate(self, atoms, properties, system_changes)

        # Prepare atom types
        z_to_atype = {35: 1, 6: 3, 20: 5, 17: 7, 9: 9, 1: 10, 53: 12, 19: 13, 3: 14, 12: 15, 7: 17, 11: 19, 8: 21, 15: 23, 16: 26}
        a_types = [ z_to_atype[z] for z in self.atoms.get_atomic_numbers() ]

        # Prepare coordinates
        coords = self.atoms.positions

        # TorchMD-NET calculation
        t_ene, t_forces = self.energy_forces(a_types, coords)

        # Store energy
        self.results['energy'] = t_ene * ase.units.kJ / ase.units.mol

        #!# Forces - set to zero for now
        natoms = len(self.atoms)
        self.results['forces'] = t_forces * ase.units.kJ / ase.units.mol

    def energy_forces(self, elem, geom):
        this_model, this_device = TorchMDNet.models[self.model_index]
        types = torch.tensor(elem, dtype=torch.long)
        types = types.to(this_device)
        pos = torch.tensor(geom, dtype=torch.float32)
        pos = pos.to(this_device)
        energy, forces = this_model.forward(types, pos)  # ,batch)
        forces = forces.detach().numpy()
        return (energy.item(), forces)



# ===============================================================================

class PM6MLCalculator(SumCalculator):

    def __init__(self, model_file, device=None):
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
            # Ml correction from TorchMDNet
            TorchMDNet(model_file=model_file, device=device)

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
model_ckpt = "/home/rezac/Github/PUBLIC/mopac-ml/models/PM6-ML_correction_seed8_best.ckpt"
atoms.calc = PM6MLCalculator(model_ckpt)
atoms_a.calc = PM6MLCalculator(model_ckpt)
atoms_b.calc = PM6MLCalculator(model_ckpt)

energy = atoms.get_potential_energy() / ase.units.kcal * ase.units.mol
energy_a = atoms_a.get_potential_energy() / ase.units.kcal * ase.units.mol
energy_b = atoms_b.get_potential_energy() / ase.units.kcal * ase.units.mol
print(energy - energy_a - energy_b)

# Gradient test
# Print analytical forces:
print("Analytical forces")
atoms.calc = TorchMDNet(model_ckpt)
forces_a = atoms.get_forces()
print(forces_a)
# Print numerical forces
print("Numerical forces")
from ase.calculators.fd import FiniteDifferenceCalculator
forces_n = ase.calculators.fd.calculate_numerical_forces(atoms, eps=1.0e-3)
print(forces_n)
# Difference
print("Difference")
print(forces_a - forces_n)
