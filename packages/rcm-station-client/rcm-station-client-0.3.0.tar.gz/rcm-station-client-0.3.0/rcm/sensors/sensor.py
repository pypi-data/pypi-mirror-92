#  Copyright (c) 2020 Pim Hazebroek
#  This program is made available under the terms of the MIT License.
#  For full details check the LICENSE file at the root of the project.
"""The base for every sensor."""

import abc

import busio
from board import SCL, SDA


class Sensor(metaclass=abc.ABCMeta):
    """
    A base class for sensors connected to the station via I2C.
    """
    def __init__(self):
        self._i2c = busio.I2C(SCL, SDA)

    @abc.abstractmethod
    def read(self):
        """
        Connect to the sensor over I2C and perform a measurement and return the value(s) that were measured.
        May return multiple values if the sensor measures multiple metrics.

        :rtype dict
        """
        raise NotImplementedError
