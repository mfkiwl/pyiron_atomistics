# coding: utf-8
# Copyright (c) Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department
# Distributed under the terms of "New BSD License", see the LICENSE file.

from pyiron_atomistics.atomistics.structure.factories.ase import AseFactory
import numpy as np

__author__ = "Liam Huber"
__copyright__ = (
    "Copyright 2021, Max-Planck-Institut für Eisenforschung GmbH - "
    "Computational Materials Design (CM) Department"
)
__version__ = "1.0.1"
__maintainer__ = "Liam Huber"
__email__ = "huber@mpie.de"
__status__ = "production"
__date__ = "Jun 28, 2021"


class LavesFactory:
    """A collection of routines for constructing Laves phase structures."""

    @staticmethod
    def C14():
        raise NotImplementedError

    @staticmethod
    def C15(element_a, element_b, a=None):
        """
        Builds a cubic $A B_2$ C15 Laves phase cell.

        Example use:
        >>> structure = C15('Al', 'Ca')
        >>> structure.repeat(2).plot3d(view_plane=([1, 1, 0], [0, 0, -1]))

        Args:
            element_a (str): The chemical symbol for the A element.
            element_b (str): The chemical symbol for the B element.
            a (float): The lattice constant. (Default is None, which uses the default nearest-neighbour distance for
                the A-type element.)

        Returns:
            (Atoms): The C15 unit cell.
        """
        bulk = AseFactory().bulk
        if a is None:
            a = bulk(name=element_a).get_neighbors(num_neighbors=1).distances[0, 0] * (4 / np.sqrt(3))

        structure = bulk(name=element_a, crystalstructure='diamond', a=a, cubic=True)
        secondary = bulk(name=element_b, crystalstructure='diamond', a=a, cubic=True)
        evens = secondary[[i for i in range(len(secondary)) if i % 2 == 0]]
        odds = secondary[[i for i in range(len(secondary)) if i % 2 == 1]]

        for shifts, sublattice in zip(
                0.125 * np.array([
                    [[-1, 3, -1], [-1, -3, 1]],
                    [[-1, -3, -1], [-1, 3, 1]]
                ]),
                [odds, evens]
        ):
            for shift in shifts:
                sub = sublattice.copy()
                sub.positions += np.dot(sub.cell.array, shift.T)
                structure += sub

        structure.wrap()
        return structure

    @staticmethod
    def C36():
        raise NotImplementedError
