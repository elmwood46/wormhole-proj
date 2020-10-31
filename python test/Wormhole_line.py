# -*- coding: utf-8 -*-
"""
@author: Ludoric
"""

import numpy as np
import cv2
import pprint


def updateProgressBar(progress):
    print('\r[{0}] {1}%'.format(('#'*int(progress*50) +
                                 ' '*(50-int(progress*50))),
          int(progress*100)), end="")


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
        return (x, y, z)
    return (x/norm, y/norm, z/norm)


def distance(a, b):
    return np.sqrt((np.subtract(a, b)**2).sum())


def add(*tups):
    return tuple(map(sum, zip(*tups)))


def mult(s, tup):
    return tuple([z * s for z in tup])


def rotate(vec, axis, theta):
    """Rodrigues' rotation formula."""
    return add(mult(np.cos(theta), vec),
               mult(np.sin(theta), np.cross(axis, vec)),
               mult((1-np.cos(theta))*np.dot(axis, vec), axis))


def r_dist(len):
    return (RHO**2+len**2)**(1/2)


Bhole = (0, 0, 0)  # black hole at (0,0,0) --by definition
up = (0, 0, 1)  # vector in the "up" direction in world space
RHO = 1  # the "size" of the wormhole

cam = (-4, 0, 0)  # camera location in cartesian coordinates
camseph = cartesianToSpherical(*cam)
# camseph = (-camseph[0], camseph[1], camseph[2])  # try starting from the other side?
camDx = normalise(*cam)  # look direction
camDy = normalise(*np.cross(up, camDx))
camDz = tuple(np.cross(camDx, camDy))
cam_Lookat = np.matmul(
    np.array([[*camDx, 0], [*camDy, 0], [*camDz, 0], [0, 0, 0, 1]]),
    np.array([[1, 0, 0, -cam[0]], [0, 1, 0, -cam[1]], [0, 0, 1, -cam[2]], [0, 0, 0, 1]]))
# print(cam)
# print(camDx, camDy, camDz)
# print(cam_Lookat)
# print(camseph)
# print(cartesianToSpherical(*camDx))

# local camera coordinates in polar form?
# direction on the cameras local sky
lenphi = 1000
ranphi = (0, 2**(1/2)*np.pi/4)
output = [0 for i in range(lenphi)]

for stepP in range(lenphi):
    camPcs = ranphi[0] + (ranphi[1]-ranphi[0])/(lenphi-1)*stepP

    # unit vector in that direction is:
    vseph = cartesianToSpherical(*camDx)
    camN = sphericalToCartesian(1, vseph[1], vseph[2]+camPcs)
    # ------------------------- I think the code is free of bugs up to here
    # little n
    n = (-camN[0], -camN[1], +camN[2])

    r = r_dist(camseph[0])  # r is the improper distance to the wormhole
    # incoming light ray's canonical momentum
    # p =  (n_l, r*n_theta, r*sin(theta)*n_phi)
    p = (n[0], r*n[1], r*np.sin(camseph[1])*n[2])
    b = p[2]  # = r*sin(theta)*n_phi
    Bsquared = (r**2)*(n[1]**2+n[2]**2)

    # numerically integrate from t=0 to t=-infinity
    # location = cam, momentum = p,  constants of motion  = (b, Bsquared)

    b = b
    Bsq = Bsquared
    (l, th, ph, Pl, Pth) = (camseph[0], camseph[1], camseph[2], p[0], p[1])
    ti = -20  # = negative infinity
    dt = -0.00817
    t = 0
    while t > ti:  # I don't know how to use for loops...
        # dl/dt = p_l
        # dtheta/dt = p_theta/r^2
        # dphi/dt = b/(r^2 sin^2(theta))
        # dP_l/dt = B^2* (dr/dl) /r^3
        # dP_theta b^2*cos(theta)/(r^2*sin^3(theta))
        r = r_dist(l)
        nl = l + Pl*dt
        (l, th, ph, Pl, Pth) = (nl,
                                th + Pth/(r**2)*dt,
                                ph + b/((r*np.sin(th))**2)*dt,
                                Pl + Bsq*((r_dist(nl)-r)/(Pl*dt) * dt)/r**3,
                                Pth + (b/r)**2*(np.cos(th)/np.sin(th)**3)*dt)
        t += dt

    updateProgressBar(stepP/lenphi)
    output[stepP] = (l, th, ph)
print()

pp = pprint.PrettyPrinter(indent=2, width=160)
pp.pprint(output)

# output now contains an array of(l', theta', phi') for (theta, phi)
width = 512
ratio = 1
fov = np.pi/2.0
height = int(width/ratio)
tx1 = cv2.imread("InterstellarWormhole_Fig6a.jpg")
tx2 = cv2.imread("InterstellarWormhole_Fig10.jpg")
img = np.zeros((width, height, 3), np.uint8)
for x in range(width):
    for y in range(height):

        x1 = int(np.floor(x/width*(lenphi-1)))
        xw = 1-(x/width*(lenphi-1) - x1)

        dir = normalise(x-width/2, y-height/2, (height/2)/np.tan(fov*0.5))
        ang_between = np.arccos(dir[2])  # np.arccos(np.dot((0,0,1), dir))
        cell = max(min(ang_between/ranphi[1], 1), 0)*(lenphi-2)
        index = int(cell)
        weight = cell - index
        # the final coordinates are linearly interpolated
        coordinate = (weight*output[index][0]+(1-weight)*output[index+1][0],
                      weight*output[index][1]+(1-weight)*output[index+1][1],
                      weight*output[index][2]+(1-weight)*output[index+1][2])
   
        orthog = normalise(*np.cross(dir, camDx))
        rayEndpoint = rotate(dir, orthog, coordinate[1])

        if(coordinate[0] < 0):
            rows, cols, channels = tx1.shape
            img[x, y] = tx1[int(((rayEndpoint[1]/(np.pi)) % 1)*rows),
                            int(((rayEndpoint[2]/(2*np.pi)+0.5) % 1)*cols)]
        else:
            rows, cols, channels = tx2.shape
            s = min(rows, cols)
            img[x, y] = tx2[int(((rayEndpoint[1]/(np.pi)) % 1)*rows),
                            int(((rayEndpoint[2]/(2*np.pi)+0.5) % 1)*cols)]
    updateProgressBar((x*width+y)/(width*height))
print()
# img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
cv2.imwrite("out.png", img)
