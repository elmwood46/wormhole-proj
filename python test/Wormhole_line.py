# -*- coding: utf-8 -*-
"""
@author: Ludoric
"""


from SphericalVectorMaths import SphVector, mult, normalise, rotate
import math
import numpy as np
import cv2
import pprint



def updateProgressBar(progress):
    print('\r[{0}] {1}%'.format(('#'*int(progress*50) +
                                 ' '*(50-int(progress*50))),
          int(progress*100)), end="")


def r_dist(len):
    return (RHO**2+len**2)**(1/2)


# Bhole = (0, 0, 0)  # black hole at (0,0,0) --by definition
RHO = 1  # the "size" of the wormhole

# cam = SphVector(4.0, math.pi/2.0, math.pi/2.0)  # camera location
cam = SphVector(4.0, math.pi/2.0, math.pi)
camDx = cam.toBasisVector_r()  # look direction
camDy = cam.toBasisVector_phi()  # unused
camDz = mult(-1, cam.toBasisVector_theta())  # unused

lenphi = 500
ranphi = (0, np.pi/2)
output = [0 for i in range(lenphi)]

for stepP in range(lenphi):
    camPcs = ranphi[0] + (ranphi[1]-ranphi[0])/(lenphi-1)*stepP

    # unit vector in that direction is:
    vseph = SphVector.fromCartesian(*camDx)
    camN = SphVector(1, vseph.theta, vseph.phi+camPcs).toCartesian()
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
    dt = -0.017
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

    updateProgressBar(stepP/lenphi)
    output[stepP] = (l, th, ph)
print()

# pp = pprint.PrettyPrinter(indent=2, width=160)
# pp.pprint(output)


# with open("out_line.csv", "w", newline="") as f:
#     for item in output:
#         f.write("{}, {}, {}\n".format(item[0], item[1], item[2]))
#     f.write('\n')


# output now contains an array of(l', theta', phi') for (theta, phi)
width = 256
ratio = 1
fov = np.pi/2.0
height = int(width/ratio)
tx1 = cv2.imread("InterstellarWormhole_Fig6a.jpg")
tx2 = cv2.imread("InterstellarWormhole_Fig10.jpg")
img = np.zeros((width, height, 3), np.uint8)

# outThing = [[0 for i in range(width)] for j in range(height)]
FDir = (1, 0, 0)
for x in range(width):
    for y in range(height):
        dir = normalise(x-width/2, y-height/2, (height/2)/math.tan(fov/2.0))
        dirs = SphVector.fromCartesian(*dir)
        ang_between = dirs.phi
        cell = max(min(ang_between/ranphi[1], 1), 0)*(lenphi-2)
        index = int(cell)
        weight = cell - index
        # the final coordinates are linearly interpolated
        coordinate = (weight*output[index][0]+(1-weight)*output[index+1][0],
                      weight*output[index][1]+(1-weight)*output[index+1][1],
                      weight*output[index][2]+(1-weight)*output[index+1][2])

        # I think the worst error is here
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
        # img[x, y] = mult(ang_between/math.pi, (255,255,255=))
    updateProgressBar((x*width+y)/(width*height))
print()
# img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
cv2.imwrite("out_line.png", img)


# with open("out_line.csv", "w", newline="") as f:
#     for sublist in outThing:
#         for item in sublist:
#             f.write("{},".format(item[0]))
#         f.write('\n')
#     f.write('\n')
#     for sublist in outThing:
#         for item in sublist:
#             f.write("{},".format(item[1]))
#         f.write('\n')
#     f.write('\n')
#     for sublist in outThing:
#         for item in sublist:
#             f.write("{},".format(item[2]))
#         f.write('\n')
#     f.write('\n')
