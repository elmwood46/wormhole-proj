# -*- coding: utf-8 -*-
"""
@author: Ludoric
"""
import math
import numpy as np


class SphVector:

    len, theta, phi = (0, 0, 0)

    def __init__(self, len, theta, phi):
        self.len = len
        self.theta = theta
        self.phi = phi

    def __str__(self):
        return("Sph: ({0}, {1}, {2})".format(self.len, self.theta, self.phi))

    def fromCartesian(x, y, z):
        """Convert Cartesian Coordinates to Spherical Coordinates."""
        r = math.sqrt(x**2+y**2+z**2)
        theta = math.acos(z/r)
        phi = math.atan2(y, x)
        return SphVector(r, theta, phi)

    def toCartesian(self):
        """Convert Spherical Coordinates to Cartesian Coordinates."""
        x = self.len*math.sin(self.theta)*math.cos(self.phi)
        y = self.len*math.sin(self.theta)*math.sin(self.phi)
        z = self.len*math.cos(self.theta)
        return (x, y, z)

    def toBasisVector_r(self):
        x = math.sin(self.theta)*math.cos(self.phi)
        y = math.sin(self.theta)*math.sin(self.phi)
        z = math.cos(self.theta)
        return (x, y, z)

    def toBasisVector_theta(self):
        x = math.cos(self.theta)*math.cos(self.phi)
        y = math.cos(self.theta)*math.sin(self.phi)
        z = -math.sin(self.phi)
        return (x, y, z)

    def toBasisVector_phi(self):
        x = -math.sin(self.phi)
        y = math.cos(self.phi)
        z = 0.0
        return (x, y, z)


def add(*tups):
    return tuple(map(sum, zip(*tups)))


def mult(s, tup):
    return tuple([z * s for z in tup])


def length(v):
    return math.sqrt(sum(e**2 for e in v))


def rotate(vec, axis, theta):
    """Rodrigues' rotation formula."""
    return add(mult(math.cos(theta), vec),
               mult(math.sin(theta), np.cross(axis, vec)),
               mult((1-math.cos(theta))*np.dot(axis, vec), axis))

def normalise(x, y, z):
    norm = math.sqrt(x**2+y**2+z**2)
    if norm == 0:
        return (x, y, z)
    return (x/norm, y/norm, z/norm)


# def distance(a, b):
#     return np.sqrt((np.subtract(a, b)**2).sum())
