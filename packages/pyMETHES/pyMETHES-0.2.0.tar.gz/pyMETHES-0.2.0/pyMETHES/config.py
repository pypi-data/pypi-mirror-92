#  Copyright (c) 2020-2021 ETH Zurich

"""
Module for the Config class of the simulation.
"""

# Import Packages
from typing import Tuple, Union
import warnings
from collections.abc import Callable
import json
import json5
import scipy.constants as csts

num = Union[int, float]


class Config:
    """
    Configuration class for the Monte-Carlo simulation.

    The configuration can be loaded from, or saved to, json or json5 files.
    Alternatively, it can be provided as, or exported to, a (nested) dictionary.
    The gas number density is not a configuration parameter, but a
    cached property of the Config class, which is computed from the pressure and
    temperature.

    Attributes:
        paths_to_cross_section_files (list): paths to the cross section files in
            txt format
        gases (list): sum formulae of gases
        fractions (list): proportions of the gases in the gas mixture
        max_cross_section_energy (float): maximum cross section energy (eV)

        output_directory (str): path to the output directory
        base_name (str): prefix of the output filename
        save_simulation_pickle (bool): save the simulation as pickle file
        save_temporal_evolution (bool): save temporal evolution
        save_swarm_parameters (bool): save swarm parameters
        save_energy_distribution (bool): save energy distribution

        EN (float): E/N ratio in (Td)
        _pressure (float): gas pressure in Pa
        _temperature (float): gas temperature in K
        _gas_number_density (float): gas number density in m-3

        num_e_initial (int): initial number of electrons
        initial_pos_electrons (list): initial position [x, y, z] of the electrons'
            center of mass
        initial_std_electrons (list): initial broadening of gaussian distributed
            electrons in x, y and z direction
        initial_energy_distribution (str): The initial energy distribution of
            the electrons. Can be either ``"zero"`` (all electrons have zero
            kinetic energy), ``"fixed"`` (all electrons have the same energy)
            or ``"maxwell-boltzmann"`` (at temperature :py:attr:`initial_temperature`).
            Maxwell-Boltzmann support is experimental, check
            :py:func:`pyMETHES.utils.maxwell_boltzmann_random` and its test case
            to see if the required precision is achieved.
            The default is ``"zero"``. If the initial distribution is `"fixed"`,
            :py:attr:`initial_energy` and :py:attr:`initial_direction` must be set.
        initial_energy (float): The initial energy of the electrons in eV.
        initial_direction (Union[Tuple[float, float, float], str]): The initial
            direction of the electrons. Either the string ``"random"`` to give
            each electron a random direction or a tuple with three elements x,
            y, z specifying a single direction for all electrons.
        initial_temperature (Union[Float, int]): The initial temperature in K. Used
            for the Maxwell-Boltzmann distribution.

        num_energy_bins (int): number of energy bins to group the electrons for the
            energy distribution
        energy_sharing_factor (float): energy sharing factor for ionization collisions
        isotropic_scattering (bool): scattering: isotropic (true), non-isotropic
            according to Vahedi et al. (false)
        conserve (bool): conservation of the number of electrons
        num_e_max (int): maximum allowed electron number (when it is reached, the
            number of electrons is then conserved until simulation ends)
        seed (int, str): optional. If set to an integer it is used to seed
            the Simulation. If set to the string `"random"` no seeding occurs.
            Default value is `"random"`.

        end_condition_type (str): Specifies the end condition. Can be
            ``"steady-state"``, ``"num_col_max"``, ``"w_tol+ND_tol"`` or
            ``"custom"``.  The ``"custom"`` end condition requires
            :py:attr:`is_done` to be set as well.  Defaults to ``"w_tol+ND_tol"``
        w_tol (float): tolerance on the flux drift velocity. simulation ends
            when w_err/w < w_tol
        DN_tol (float): tolerance on the flux diffusion coefficient. simulation ends
            when DN_err/w < DN_tol
        num_col_max (int): maximum number of collisions during the simulation,
            simulation ends when it is reached
        is_done (Callable): This function gets called to determine whether to end the
            simulation or not. Gets passed the simulation object as argument.
            Return ``True`` to stop the simulation, ``False`` otherwise.
        timeout (int): End the simulation after ``timeout`` seconds. Zero means no
            timeout. Defaults to zero.
    """

    def __init__(self, config: Union[str, dict]):
        """
        Instantiate the config.

        Args:
            config (str, dict): path to a json or json5 config file, or dictionary.
        """

        if isinstance(config, str):
            if config.endswith('.json5'):
                with open(config, "r") as json_file:
                    config = json5.load(json_file)
            elif config.endswith('.json'):
                with open(config, "r") as json_file:
                    config = json.load(json_file)
            else:
                raise ValueError(f"Configuration file '{config}' has invalid extension."
                                 " Extensions '.json' or '.json5' are expected.")

        # gases
        input_gases = config['input_gases']
        self.paths_to_cross_section_files: list = \
            input_gases['paths_to_cross_section_files']
        self.gases: list = input_gases['gases']
        self.fractions: list = input_gases['fractions']
        self.max_cross_section_energy: float = \
            float(input_gases['max_cross_section_energy'])

        # output
        output = config['output']
        self.output_directory: str = output['output_directory']
        self.base_name: str = output['base_name']
        self.save_simulation_pickle: bool = output['save_simulation_pickle']
        self.save_temporal_evolution: bool = output['save_temporal_evolution']
        self.save_swarm_parameters: bool = output['save_swarm_parameters']
        self.save_energy_distribution: bool = output['save_energy_distribution']

        # physical conditions
        physical_conditions = config['physical_conditions']
        self.EN: float = float(physical_conditions['EN'])
        self._pressure: float = float(physical_conditions['pressure'])
        self._temperature: float = float(physical_conditions['temperature'])
        self._gas_number_density: float = None

        # initial state
        initial_state = config['initial_state']
        self.num_e_initial: int = int(initial_state['num_e_initial'])
        self.initial_pos_electrons: list = initial_state['initial_pos_electrons']
        self.initial_std_electrons: list = initial_state['initial_std_electrons']
        self.initial_energy_distribution: str = "zero"
        self.initial_energy: float = None
        self.initial_direction: Union[Tuple[float, float, float], str] = None
        self.initial_temperature: Union[int, float] = None

        if 'initial_energy_distribution' in initial_state:
            val = initial_state['initial_energy_distribution']

            if val not in ("zero", "fixed", "maxwell-boltzmann"):
                raise ValueError(
                    "initial_energy_distribution must be zero, fixed or "
                    "maxwell-boltzmann")

            self.initial_energy_distribution = val

        if 'initial_energy' in initial_state and \
                initial_state['initial_energy'] is not None:
            self.initial_energy = float(initial_state['initial_energy'])
            if self.initial_energy < 0:
                raise ValueError("initial_energy cannot be negative")

        if 'initial_direction' in initial_state and \
                initial_state['initial_direction'] is not None:
            val = initial_state['initial_direction']

            if isinstance(val, str) and val == "random":
                self.initial_direction = val
            elif isinstance(val, (list, tuple)):
                if len(val) != 3:
                    raise ValueError("initial_direction must be \"random\" "
                                     "or list of three floats")

                self.initial_direction = [float(item) for item in val]

                if self.initial_direction == [0, 0, 0]:
                    raise ValueError("initial_direction cannot be all zero")
            else:
                raise ValueError("Invalid value for initial_direction")

        if 'initial_temperature' in initial_state:
            self.initial_temperature = float(initial_state['initial_temperature'])

            if self.initial_temperature < 0:
                raise ValueError("initial_temperature must be positive")

        if self.initial_energy_distribution in ("zero", "maxwell-boltzmann"):
            if self.initial_energy is not None:
                warnings.warn("initial_energy setting useless with "
                              f"{self.initial_energy_distribution} distribution")
            if self.initial_direction is not None:
                warnings.warn("initial_direction setting useless with "
                              f"{self.initial_energy_distribution} distribution")
        else:
            assert self.initial_energy_distribution == "fixed"
            if self.initial_energy is None:
                raise ValueError("Must set initital_energy")
            if self.initial_direction is None:
                raise ValueError("Must set initial_direction")

        if self.initial_energy_distribution == "maxwell-boltzmann" and \
                self.initial_temperature is None:
            raise ValueError("Must set initial_temperature for Maxwell-Boltzmann")

        # simulation settings
        simulation = config['simulation_settings']
        self.num_energy_bins: int = simulation['num_energy_bins']
        self.energy_sharing_factor: float = float(simulation['energy_sharing_factor'])
        self.isotropic_scattering: bool = simulation['isotropic_scattering']
        self.conserve: bool = simulation['conserve']
        self.num_e_max: int = int(simulation['num_e_max'])
        self.seed: Union[int, str] = "random"
        if 'seed' in simulation:
            seed = simulation['seed']
            if isinstance(seed, int) or (isinstance(seed, str) and seed == "random"):
                self.seed = seed
            else:
                raise ValueError("seed must be an integer or the string \"random\"")

        # end conditions
        end_conditions = config['end_conditions']
        self.end_condition_type: str = "w_tol+ND_tol"

        if 'end_condition_type' in end_conditions:
            val = str(end_conditions['end_condition_type'])

            if val not in ("steady-state", "num_col_max", "w_tol+ND_tol", "custom"):
                raise ValueError("end_condition_type must be \"steady-state\", "
                                 "\"num_col_max\", \"w_tol+ND_tol\" or \"custom\"")

            self.end_condition_type = val

        self.w_tol: float = float(end_conditions['w_tol'])
        self.DN_tol: float = float(end_conditions['DN_tol'])
        self.num_col_max: int = int(end_conditions['num_col_max'])
        self.is_done: Callable = None
        self.timeout: int = 0

        if 'is_done' in end_conditions and end_conditions['is_done'] is not None:
            self.is_done = end_conditions['is_done']

            if not isinstance(self.is_done, Callable):
                raise TypeError("is_done must be a function")

        if self.end_condition_type == "custom" and self.is_done is None:
            raise ValueError("custom requires is_done to be set to a callback")
        elif self.end_condition_type != "custom" and self.is_done is not None:
            warnings.warn("Setting is_done is useless without end_condition_type "
                          "custom")

        if 'timeout' in end_conditions:
            self.timeout = int(end_conditions['timeout'])

            if self.timeout < 0:
                raise ValueError("timeout must be >= 0")

    @property
    def gas_number_density(self) -> float:
        if self._gas_number_density is None:
            self._gas_number_density = \
                self.pressure / (csts.Boltzmann * self.temperature)
        return self._gas_number_density

    @property
    def pressure(self) -> float:
        return self._pressure

    @pressure.setter
    def pressure(self, value: float):
        """
        Pressure setter. If a new value is set, resets the cache for the gas
        number density.

        Args:
            value: pressure in Pascal
        """
        self._pressure = value
        self._gas_number_density = None

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        """
        Temperature setter. If a new value is set, resets the cache for the gas
        number density.

        Args:
            value: temperature in Kelvin
        """
        self._temperature = value
        self._gas_number_density = None

    def to_dict(self) -> dict:
        """
        Returns the current configuration as a dictionary.

        Returns: dict of configuration
        """

        return {
            'input_gases': {
                'gases': self.gases,
                'paths_to_cross_section_files': self.paths_to_cross_section_files,
                'fractions': self.fractions,
                'max_cross_section_energy': self.max_cross_section_energy,
            },
            'output': {
                'output_directory': self.output_directory,
                'base_name': self.base_name,
                'save_simulation_pickle': self.save_simulation_pickle,
                'save_temporal_evolution': self.save_temporal_evolution,
                'save_swarm_parameters': self.save_swarm_parameters,
                'save_energy_distribution': self.save_energy_distribution,
            },
            'physical_conditions': {
                'EN': self.EN,
                'pressure': self.pressure,
                'temperature': self.temperature,
            },
            'initial_state': {
                'num_e_initial': self.num_e_initial,
                'initial_pos_electrons': self.initial_pos_electrons,
                'initial_std_electrons': self.initial_std_electrons,
                'initial_energy_distribution': self.initial_energy_distribution,
                'initial_energy': self.initial_energy,
                'initial_direction': self.initial_direction,
            },
            'simulation_settings': {
                'num_energy_bins': self.num_energy_bins,
                'energy_sharing_factor': self.energy_sharing_factor,
                'isotropic_scattering': self.isotropic_scattering,
                'conserve': self.conserve,
                'num_e_max': self.num_e_max,
                'seed': self.seed,
            },
            'end_conditions': {
                'end_condition_type': self.end_condition_type,
                'w_tol': self.w_tol,
                'DN_tol': self.DN_tol,
                'num_col_max': self.num_col_max,
                'is_done': self.is_done,
            }
        }

    def save_json5(self, path: str = 'config.json5') -> None:
        """
        Saves the current configuration to a json5 file.

        Args:
            path (str): path including the file name and extension,
                example: 'data/config.json5'
        """

        d = self.to_dict()

        if d['end_conditions']['is_done'] is not None:
            del d['end_conditions']['is_done']
            warnings.warn("Cannot save custom callback to json5!")

        with open(path, "w") as config_file:
            json5.dump(d, config_file, indent=2)

    def save_json(self, path: str = 'config.json') -> None:
        """
        Saves the current configuration to a json file.

        Args:
            path (str): path including the file name and extension,
                example: 'data/config.json'
        """

        d = self.to_dict()

        if d['end_conditions']['is_done'] is not None:
            del d['end_conditions']['is_done']
            warnings.warn("Cannot save custom callback to json!")

        with open(path, "w") as config_file:
            json.dump(d, config_file, indent=2)
