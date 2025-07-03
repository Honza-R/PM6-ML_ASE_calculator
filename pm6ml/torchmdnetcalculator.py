import torch
from torchmdnet.models.model import load_model
from ase.calculators.calculator import Calculator, all_changes
import ase.units

class TorchMDNetCalculator(Calculator):

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
        if not self.model_index in self.__class__.models:
            # Device to be used
            if device:
                new_device = torch.device(device)
            else:
                new_device = torch.get_default_device()
            # Load model
            new_model = load_model(model_file, derivative=True)
            new_model.to(new_device)
            self.__class__.models[self.model_index] = (new_model, new_device)

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
        this_model, this_device = self.__class__.models[self.model_index]
        types = torch.tensor(elem, dtype=torch.long)
        types = types.to(this_device)
        pos = torch.tensor(geom, dtype=torch.float32)
        pos = pos.to(this_device)
        energy, forces = this_model.forward(types, pos)  # ,batch)
        forces = forces.detach().numpy()
        return (energy.item(), forces)

