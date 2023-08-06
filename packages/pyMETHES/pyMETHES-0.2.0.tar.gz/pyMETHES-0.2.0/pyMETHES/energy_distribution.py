#  Copyright (c) 2020-2021 ETH Zurich

"""
Module for the InstantaneousEnergyDistribution and TimeAveragedEnergyDistribution
classes.

Both classed inherit from the abstract class EnergyDistribution. The
InstantaneousEnergyDistribution class can be used to calculate the eedf and eepf
at a given point in time. The TimeAveragedEnergyDistribution class allows for
averaging the eedf and eepf over time. This is done by updating an histogram of
electron energies at every time-step.
"""

# Import Packages
from abc import ABC
import numpy as np

np.seterr(all='raise')


class EnergyDistribution(ABC):
    """
    Abstract base class for electron energy distributions.

    Attributes:
        energy_bins (ndarray): bins to construct the histogram of electron energies
        energy_bin_centers (ndarray): centers of the energy bins (length - 1)
        eedf (ndarray): electron energy distribution function (eV-1)
        eepf (ndarray): electron energy probability function (eV-3/2)
    """

    def __init__(self):
        self.energy_bins = None
        self.energy_bin_centers = None
        self.eedf = None
        self.eepf = None

    def calculate_bin_centers(self) -> None:
        """
        Calculate the center values of the energy bins.
        """

        self.energy_bin_centers = 0.5 * (self.energy_bins[1:] + self.energy_bins[:-1])


class InstantaneousEnergyDistribution(EnergyDistribution):
    """
    Stores the energy distribution of electrons.
    """

    def calculate_distribution(self, energies, energy_bins=None) -> None:
        """
        Calculates the eedf and eepf associated to the input electron energies.

        Args:
            energies (ndarray): array of electron energies
            energy_bins (ndarray): (optional) energy bins for calculating the eedf
                and eepf. If None, the energy bins are automatically determined with the
                Freedman Diaconis Estimator.
        """

        self.eepf = None
        if energy_bins is None:
            (self.eedf, self.energy_bins) = np.histogram(energies, bins='fd',
                                                         density=True)
        else:
            self.energy_bins = energy_bins
            self.eedf = np.histogram(energies, bins=energy_bins, density=True)[0]
        self.calculate_bin_centers()
        if 0 not in self.energy_bin_centers:
            self.eepf = self.eedf / np.sqrt(self.energy_bin_centers)


class TimeAveragedEnergyDistribution(EnergyDistribution):
    """
    Stores the energy distribution of electrons (averaged over time after swarm
    equilibration).

    Attributes:
        cumulative_energy_histogram (ndarray): energy histogram cumulated over every
            time-step since steady-state
    """

    def __init__(self):
        super().__init__()
        self.cumulative_energy_histogram = 0
        self.energy_mean = None
        self.energy_mean_err = None

    def generate_bins(self, num_bins: int, max_energy: float) -> None:
        """
        Generate fixed energy bins for averaging the eedf over time. The bins are
        spaced linearly and range from 0 to 150% of the maximum electron energy at the
        step where the method is called.

        Args:
            num_bins (int): number of energy bins
            max_energy (float): maximum electron energy (eV)
        """

        self.energy_bins = np.linspace(0, 1.5 * max_energy, num_bins)
        self.calculate_bin_centers()

    def collect_histogram(self, energies) -> None:
        """
        Updates the current eedf and eepf, using the electron energies given as input.
        The energy bins should be already defined and are re-used. This method should
        be called at every time-step.

        Args:
            energies (ndarray): array of electron energies
        """

        self.cumulative_energy_histogram += np.histogram(energies,
                                                         bins=self.energy_bins)[0]

    def calculate_distribution(self, mean_energies: np.ndarray) -> None:
        """
        Calculates the eedf and eepf using the cumulative energy histogram.
        Calculates the mean electron energy averaged over time.

        Args:
            mean_energies (ndarray): mean energies at every time-step after
                swarm equilibration
        """

        integral = sum(self.cumulative_energy_histogram * np.diff(self.energy_bins))
        self.eedf = self.cumulative_energy_histogram
        if integral != 0:
            self.eedf = self.eedf / integral
        if 0 not in self.energy_bin_centers:
            self.eepf = self.eedf / np.sqrt(self.energy_bin_centers)

        # calculate the mean energy
        self.energy_mean = np.mean(mean_energies)

        # At least 10 steps are required to estimate the errors
        if mean_energies.size > 9:
            # calculate the mean energy error
            self.energy_mean_err = np.std(mean_energies) / np.sqrt(mean_energies.size)
