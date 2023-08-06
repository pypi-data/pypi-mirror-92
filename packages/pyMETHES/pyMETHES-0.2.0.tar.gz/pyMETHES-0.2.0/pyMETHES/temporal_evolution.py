#  Copyright (c) 2020-2021 ETH Zurich

"""
Module for the TimeSeries class.
"""

# Import Packages
import numpy as np
import pandas as pd

# Import modules
from pyMETHES.electrons import Electrons


class TimeSeries:
    """
    Temporal evolution of some quantities during the simulation.

    The TimeSeries class stores the temporal evolution of some quantities in arrays of
    ever-increasing length. The TimeSeries can be exported to a pandas DataFrame for
    further processing.

    Attributes:
        ind_equ (int): index of equilibration time
        time (ndarray): simulated time
        num_collisions (ndarray): cumulative number of collisions
        num_electrons (ndarray): number of electrons
        num_cations (ndarray): cumulative number of cations
        num_anions (ndarray): cumulative number of anions
        mean_energy (ndarray): mean energy of electrons
        mean_position (ndarray): mean position of electrons
        var_position (ndarray): variance of electrons positions
        mean_velocity (ndarray): mean velocity of electrons
        mean_velocity_moment (ndarray): mean velocity moment of electrons
    """

    def __init__(self, electrons: Electrons):
        """
        Instantiates a TimeSeries.

        Args:
            electrons (Electrons): electron related data
        """

        # number of time steps until equilibration
        self.ind_equ = None

        self.time = np.array([0])
        self.num_collisions = np.array([0])
        self.num_electrons = np.array([electrons.num_e])
        self.num_cations = np.array([0])
        self.num_anions = np.array([0])
        self.mean_energy = np.array([electrons.mean_energy])
        self.mean_position = electrons.mean_position
        self.var_position = electrons.var_position
        self.mean_velocity = electrons.mean_velocity
        self.mean_velocity_moment = electrons.mean_velocity_moment

    def append_data(self, electrons: Electrons, dt: float, n_coll: int, n_cations: int,
                    n_anions: int) -> None:
        """
        Appends latest data to the arrays storing the temporal evolution of some
        quantities.

        Args:
            electrons (Electrons): current data related to the electrons
            dt (float): duration of the current time-step (s)
            n_coll (int): number of collisions during the current time-step
            n_cations (int): number of cations produced during the current time-step
            n_anions (int): number of anions produced during the current time-step
        """

        self.time = np.append(self.time, self.time[-1] + dt)
        self.num_collisions = np.append(self.num_collisions,
                                        self.num_collisions[-1] + n_coll)
        self.num_electrons = np.append(self.num_electrons, electrons.num_e)
        self.num_cations = np.append(self.num_cations,
                                     self.num_cations[-1] + n_cations)
        self.num_anions = np.append(self.num_anions,
                                    self.num_anions[-1] + n_anions)
        self.mean_energy = np.append(self.mean_energy, electrons.mean_energy)
        self.mean_position = np.vstack([self.mean_position, electrons.mean_position])
        self.var_position = np.vstack([self.var_position, electrons.var_position])
        self.mean_velocity = np.vstack([self.mean_velocity, electrons.mean_velocity])
        self.mean_velocity_moment = np.vstack([self.mean_velocity_moment,
                                               electrons.mean_velocity_moment])

    def to_dataframe(self) -> pd.DataFrame:
        """
        Creates a pandas DataFrame with the data containe in the TimeSeries and
        returns it.

        Returns: pandas DataFrame containing the TimeSeries data.
        """

        n = self.time.size
        num_coll = np.diff(self.num_collisions, prepend=0)
        num_null_coll = self.num_electrons - num_coll

        df = pd.DataFrame(data=np.concatenate([
            self.time.reshape((n, 1)),
            num_coll.reshape((n, 1)),
            num_null_coll.reshape((n, 1)),
            self.num_electrons.reshape((n, 1)),
            self.num_cations.reshape((n, 1)),
            self.num_anions.reshape((n, 1)),
            self.mean_energy.reshape((n, 1)),
            self.mean_position,
            self.var_position,
            self.mean_velocity,
            self.mean_velocity_moment
        ], axis=1), columns=[
            'time',
            'num_collisions',
            'num_null_collisions',
            'num_electrons',
            'num_cations',
            'num_anions',
            'mean_energy',
            'mean_position_x',
            'mean_position_y',
            'mean_position_z',
            'var_position_x',
            'var_position_y',
            'var_position_z',
            'mean_velocity_x',
            'mean_velocity_y',
            'mean_velocity_z',
            'mean_velocity_moment_x',
            'mean_velocity_moment_y',
            'mean_velocity_moment_z',
        ])
        df.attrs = {'index_equilibration': self.ind_equ}
        return df
