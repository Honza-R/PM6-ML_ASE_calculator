#!/usr/bin/env python3

import os
from ase.calculators.mixing import SumCalculator
from ase.calculators.mopac import MOPAC

# DFTD3 from simple-dftd3 package:
from dftd3.ase import DFTD3

# TorchMDNet calculator:
from pm6ml import TorchMDNetCalculator

# Modify MOPAC calculator to hide also the stdout
MOPAC._legacy_default_command = "mopac PREFIX.mop 2> /dev/null > /dev/null"


class PM6MLCalculator(SumCalculator):

    PM6ML_D3_PARAMETERS = {
        "s6": 1.0,
        "s8": 0.3908,
        "a1": 0.566,
        "a2": 3.128,
        "s9": 1.0,
        "alp": 16.0,
    }

    def __init__(self, model_file=None, device=None):
        # Look for model file
        if model_file:
            # If model is passed as the argument, use it
            if not os.path.isfile(model_file):
                raise RuntimeError(
                    "PM6MLCalculator init: model file passed as an argument does not exist"
                )
        else:
            # If not, try getting it from an environment variable
            env_model_file = os.getenv("PM6ML_MODEL")
            if env_model_file:
                if not os.path.isfile(env_model_file):
                    raise RuntimeError(
                        "PM6MLCalculator init: model file specified in PM6ML_MODEL environment variable does not exist"
                    )
                model_file = env_model_file
            else:
                raise RuntimeError("No model file provided for the ML correction.")

        # List of calculators to combine
        calcs = [
            # PM6 calculation in MOPAC
            MOPAC(label="calc_mopac", method="PM6"),
            # DFTD3 from simple-dftd3 package:
            DFTD3(damping="d3bj", params_tweaks=self.__class__.PM6ML_D3_PARAMETERS),
            # Ml correction from TorchMDNet
            TorchMDNetCalculator(model_file=model_file, device=device),
        ]
        # Initialize the calculators
        super().__init__(calcs)
