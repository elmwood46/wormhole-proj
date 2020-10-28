# -*- coding: utf-8 -*-
"""
@author: Ludoric
"""

import numpy as np
import cv2
import math
import pprint


def cartesianToSpherical(x, y, z):
    """Convert Cartesian Coordinates to Spherical Coordinates."""
    r = np.sqrt(x**2+y**2+z**2)
    theta = np.arccos(z/r)
    phi = np.arctan2(y, x)
    return r, theta, phi


def sphericalToCartesian(r, theta, phi):
    """Convert Spherical Coordinates to Cartesian Coordinates."""
    x = r*np.sin(theta)*np.cos(phi)
    y = r*np.sin(theta)*np.sin(phi)
    z = r*np.cos(theta)
    return x, y, z


def normalise(x, y, z):
    norm = np.sqrt(x**2+y**2+z**2)
    if norm == 0:
        return x, y, z
    return (x/norm, y/norm, z/norm)


def distance(a, b):
    return np.sqrt((np.subtract(a, b)**2).sum())


def add(*tups):
    return tuple(map(sum, zip(*tups)))
def mult(s, tup):
    return tuple([z * s for z in tup])


Bhole = (0, 0, 0)  # black hole at (0,0,0)
up = (0, 0, 1)  # vector in the "up" direction in world space

cam = (1, 0, 0)  # camera location in cartesian coordinates
camDx = normalise(*np.subtract(cam, Bhole))  # look direction
camDy = normalise(*np.cross(up, camDx))
camDz = tuple(np.cross(camDx, camDy))
cam_Lookat = np.matmul(
    np.array([[*camDy, 0], [*camDz, 0], [*camDx, 0], [0, 0, 0, 1]]),
    np.array([[1, 0, 0, -cam[0]], [0, 1, 0, -cam[1]], [0, 0, 1, -cam[2]], [0, 0, 0, 1]]))
camseph = cartesianToSpherical(*cam)  # (1, pi/2, 0)


# local camera coordinates in polar from?
# direction on the cameras local sky
# camPcs = 0
# camTcs = 0
lenphi, lentheta = 16, 16
ranphi, rantheta = (-np.pi/4, np.pi/4), (-np.pi/4, np.pi/4)
output = [[(0, 0, 0)] * lenphi]*lentheta
for stepT in range(lentheta):
    camTcs = rantheta[0] + (rantheta[1]-rantheta[0])/lentheta*stepT
    for stepP in range(lenphi):
        camPcs = ranphi[0] + (ranphi[1]-ranphi[0])/lenphi*stepP

        # unit vector in that direction is:
        vseph = cartesianToSpherical(*camDx)
        camN = sphericalToCartesian(1, vseph[1]+camTcs, vseph[2]+camPcs)  # ---------------------------- I think the code is free of bugs up to here
        # print((vseph[1]+camTcs, vseph[2]+camPcs))
        # little n
        n = (-camN[0], -camN[1], camN[2])
        # if(camPcs==0 and camTcs==0):
        # print(n)

        r = distance(Bhole, cam)  # r is the improper distance to the wormhole (I think)
        # incoming light ray's canonical momentum
        p = (n[0], r*n[1], r*np.sin(camTcs)*n[2])
        b = p[2]  # = r*np.sin(theta)*n[2]
        Bsquared = r**2*(n[1]**2+n[2]**2)

        # numerically integrate from t=0 to t=-infinity
        # location = cam, momentum = p,  constants of motion (b, Bsquared)

        # dl/dt = p_l
        # dtheta/dt = p_theta/r^2
        # dphi/dt = b/(r^2 sin^2(theta))
        # dP_l/dt = B^2* (dr/dl) /r^3
        # dP_theta b^2*cos(theta)/(r^2*sin^3(theta))


        b = b
        Bsq = Bsquared
        (l, th, ph, Pl, Pth) = (camseph[0], camseph[1], camseph[2], p[0], p[1])
        ti = -100  # = negative infinity
        dt = -0.1
        t = 0
        # print(th)
        while t > ti:  # I don't know how to use for loops...
            r = distance(Bhole, sphericalToCartesian(l, th, ph))
            # break
            nl = l + Pl*dt
            nth = th + Pth/r**2*dt
            nph = ph + b/(r*np.sin(th))**2*dt
            dr = distance(Bhole, sphericalToCartesian(nl, nth, nph))-r
            (l, th, ph, Pl, Pth) = (nl,
                                    nth,
                                    nph,
                                    Pl + Bsq*(dr/Pl*dt)/r**3,
                                    Pth + b**2*np.cos(th)/(r**2*np.sin(th)**3))
            t += dt

        output[stepP][stepT] = (l, th, ph)

pp = pprint.PrettyPrinter(indent=2, width=160)
pp.pprint(output)
# output now contains an array of all (l', theta', phi') showing which part of each image to sample
tx1 = cv2.imread("tex1.jpg")
tx2 = cv2.imread("tex2.png")
img = np.zeros((256, 256, 3), np.uint8)
for x in range(256):
    x1 = math.floor(x/256*(lenphi-1))
    xw = 1-(x/256*(lenphi-1) - x1)  # weight for x vs x+1
    for y in range(256):
        y1 = math.floor(y/256*(lentheta-1))
        yw = 1-(y/256*(lentheta-1) - y1)
        coordinates = add(mult(xw*yw, output[x1][y1]),
                          mult(xw*(1-yw), output[x1][y1+1]),
                          mult((1-xw)*yw, output[x1+1][y1]),
                          mult((1-xw)*(1-yw), output[x1+1][y1+1]))
        if(coordinates[0] < 0):
            img[x, y] = [0, 0, 0]
        else:
            img[x, y] = [255, 255, 255]

cv2.imwrite("out.png", img)
