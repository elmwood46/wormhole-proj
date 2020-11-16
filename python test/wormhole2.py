# -*- coding: utf-8 -*-
"""
@author: Ludoric
"""

from SphericalVectorMaths import SphVector, mult, add  # ,length
import math
import numpy as np
import cv2
import pprint


def r_dist(len):
    return (RHO**2+len**2)**(1/2)


# Bhole = (0, 0, 0)  # black hole at (0,0,0) --by definition
RHO = 1  # the "size" of the wormhole

# cam = SphVector(4.0, math.pi/2.0, math.pi/2.0)  # camera location
cam = SphVector(4.0, math.pi/2.0, math.pi)
camDx = cam.toBasisVector_r()  # look direction
camDy = cam.toBasisVector_phi()  # unused
camDz = mult(-1, cam.toBasisVector_theta())  # unused


# local camera coordinates in polar form?
# direction on the cameras local sky
lenphi, lentheta = 32, 32
ranphi, rantheta = (-math.pi/4, math.pi/4), (-math.pi/4, math.pi/4)  # ranges
output = [[0 for i in range(lentheta)] for j in range(lenphi)]
for stepT in range(lentheta):
    camTcs = rantheta[0] + (rantheta[1]-rantheta[0])/(lentheta-1)*stepT
    for stepP in range(lenphi):
        camPcs = ranphi[0] + (ranphi[1]-ranphi[0])/(lenphi-1)*stepP

        # unit vector in that direction is:
        vseph = SphVector.fromCartesian(*camDx)
        camN = SphVector(1, vseph.theta+camTcs, vseph.phi+camPcs).toCartesian()
        # camN = SphVector(1, math.pi/2.0+camTcs, 2.0*math.pi/2.0+camPcs).toCartesian()
        # little n
        nhat = SphVector(-camN[0], +camN[2], -camN[1])

        r = r_dist(cam.len)  # r is the improper distance to the wormhole
        # incoming light ray's canonical momentum
        # p =  (n_l, r*n_theta, r*sin(theta)*n_phi)
        p = SphVector(nhat.len, r*nhat.theta, r*math.sin(cam.theta)*nhat.phi)
        b = p.phi  # = r*sin(theta)*n_phi
        Bsquared = (r**2)*(nhat.theta**2+nhat.phi**2)
        # Bsquared = (p.theta**2+(p.phi/math.sin(cam.theta))**2)

        # numerically integrate from t=0 to t=-infinity
        # location = cam, momentum = p,  constants of motion  = (b, Bsquared)

        b = b
        Bsq = Bsquared
        (l, th, ph, Pl, Pth) = (cam.len, cam.theta, cam.phi, p.len, p.theta)
        # print(vseph)
        ti = -20  # = negative infinity
        dt = -0.027
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
                                    ph + b/((r*math.sin(th))**2)*dt,
                                    Pl + Bsq*((r_dist(nl)-r)/(Pl*dt)*dt)/r**3,
                                    Pth + (b/r)**2*(math.cos(th)/math.sin(th)**3)*dt)
            t += dt

        print(stepT*lentheta+stepP)
        output[stepP][stepT] = (l, th, ph)


pp = pprint.PrettyPrinter(indent=2, width=160)
pp.pprint(output)

with open("out.csv", "w", newline="") as f:
    for sublist in output:
        for item in sublist:
            f.write("{},".format(item[0]))
        f.write('\n')
    f.write('\n')
    for sublist in output:
        for item in sublist:
            f.write("{},".format(item[1]))
        f.write('\n')
    f.write('\n')
    for sublist in output:
        for item in sublist:
            f.write("{},".format(item[2]))
        f.write('\n')
    f.write('\n')

# output now contains an array of(l', theta', phi') for (theta, phi)
width = 512
ratio = 1
fov = 90 / 180*math.pi
height = int(width/ratio)
tx1 = cv2.imread("InterstellarWormhole_Fig6a.jpg")
tx2 = cv2.imread("InterstellarWormhole_Fig10.jpg")
img = np.zeros((width, height, 3), np.uint8)

for x in range(width):
    for y in range(height):

        x1 = int(math.floor(x/width*(lenphi-1)))
        xw = 1-(x/width*(lenphi-1) - x1)
        y1 = int(math.floor(y/height*(lentheta-1)))
        yw = 1-(y/height*(lentheta-1) - y1)

        # (dx, dy, dz) = (x-width/2, height/2-y, -(height/2)/math.tan(fov*0.5))
        # dir = cartesianToSpherical((dx, dy, dz))
        # this is not a very good camera, it projects onto a spherical screen

        # the final coordinates are linearly interpolatedg from the small grid
        coordinates = add(mult(xw*yw, output[x1][y1]),
                          mult(xw*(1-yw), output[x1][y1+1]),
                          mult((1-xw)*yw, output[x1+1][y1]),
                          mult((1-xw)*(1-yw), output[x1+1][y1+1]))
        coordinates = (coordinates[0], coordinates[1], coordinates[2]-4)
        if(coordinates[0] < 0):
            rows, cols, channels = tx1.shape
            img[x, y] = tx1[int(((coordinates[1]/(math.pi)) % 1)*rows),
                            int(((coordinates[2]/(2*math.pi)+0.5) % 1)*cols)]
        else:
            rows, cols, channels = tx2.shape
            s = min(rows, cols)
            img[x, y] = tx2[int(((coordinates[1]/(math.pi)) % 1)*rows),
                            int(((coordinates[2]/(2*math.pi)+0.5) % 1)*cols)]

# img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
cv2.imwrite("out.png", img)
