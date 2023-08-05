import numpy as np
cimport numpy as np
cimport cython
from yt.funcs import get_pbar

cdef extern from "math.h":
    double sqrt(double x) nogil
    double sin(double x) nogil
    double cos(double x) nogil
    double atan(double x) nogil
    double atan2(double y, double x) nogil
    double asin(double x) nogil

    
@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
def doppler_shift(np.ndarray[np.float64_t, ndim=1] shift,
                  np.ndarray[np.int64_t, ndim=1] n_ph,
                  np.ndarray[np.float64_t, ndim=1] eobs):

    cdef np.int64_t num_cells = n_ph.shape[0]
    cdef np.float64_t shft
    cdef np.int64_t i, j, k

    pbar = get_pbar("Doppler shifting photons", num_cells)

    k = 0
    for i in range(num_cells):
        shft = sqrt((1.-shift[i])/(1.+shift[i]))
        for j in range(n_ph[i]):
            eobs[k] = eobs[k] * shft
            k += 1
        pbar.update()
    pbar.finish()

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
def scatter_events(normal, prng, kernel, data_type,
                   int num_det,
                   np.ndarray[np.uint8_t, cast=True] det,
                   np.ndarray[np.int64_t, ndim=1] n_ph,
                   np.ndarray[np.float64_t, ndim=2] pos,
                   np.ndarray[np.float64_t, ndim=1] dx,
                   np.ndarray[np.float64_t, ndim=1] x_hat,
                   np.ndarray[np.float64_t, ndim=1] y_hat):

    cdef np.int64_t num_cells = dx.shape[0]
    cdef np.ndarray[np.float64_t, ndim=1] xsky, ysky, zsky
    cdef np.int64_t i, j, k, xax, yax, n
    cdef np.float64_t xx, yy

    k = 0
    n = 0

    pbar = get_pbar("Generating event positions", num_cells)

    if isinstance(normal, int):

        if normal == 0:
            xax = 1
            yax = 2
        elif normal == 1:
            xax = 2
            yax = 0
        elif normal == 2:
            xax = 0
            yax = 1
    
        if data_type == "cells":
            xsky = prng.uniform(low=-0.5, high=0.5, size=num_det)
            ysky = prng.uniform(low=-0.5, high=0.5, size=num_det)
        elif data_type == "particles":
            if kernel == "gaussian":
                xsky = prng.normal(loc=0.0, scale=1.0, size=num_det)
                ysky = prng.normal(loc=0.0, scale=1.0, size=num_det)
            elif kernel == "top_hat":
                r = prng.uniform(low=0.0, high=1.0, size=num_det)
                theta = 2.0*np.pi*prng.uniform(low=0.0, high=1.0, size=num_det)
                xsky = r*np.cos(theta)
                ysky = r*np.sin(theta)
    
        for i in range(num_cells):
            for j in range(n_ph[i]):
                if det[n]:
                    xsky[k] = xsky[k]*dx[i] + pos[i, xax]
                    ysky[k] = ysky[k]*dx[i] + pos[i, yax]
                    k += 1
                n += 1
            pbar.update()

    else:
    
        if data_type == "cells":
            xsky, ysky, zsky = prng.uniform(low=-0.5, high=0.5, 
                                            size=(3, num_det))
            for i in range(num_cells):
                for j in range(n_ph[i]):
                    if det[n]:
                        xsky[k] = xsky[k]*dx[i] + pos[i, 0]
                        ysky[k] = ysky[k]*dx[i] + pos[i, 1]
                        zsky[k] = zsky[k]*dx[i] + pos[i, 2]
                        xx = (xsky[k]*x_hat[0]+ ysky[k]*x_hat[1]+
                              zsky[k]*x_hat[2])
                        yy = (xsky[k]*y_hat[0]+ ysky[k]*y_hat[1]+
                              zsky[k]*y_hat[2])
                        xsky[k] = xx
                        ysky[k] = yy
                        k += 1
                    n += 1
                pbar.update()
        elif data_type  == "particles":
            if kernel == "gaussian":
                xsky = prng.normal(loc=0.0, scale=1.0, size=num_det)
                ysky = prng.normal(loc=0.0, scale=1.0, size=num_det)
            elif kernel == "top_hat":
                r = prng.uniform(low=0.0, high=1.0, size=num_det)
                theta = 2.0*np.pi*prng.uniform(low=0.0, high=1.0, size=num_det)
                xsky = r*np.cos(theta)
                ysky = r*np.sin(theta)
            for i in range(num_cells):
                for j in range(n_ph[i]):
                    if det[n]:
                        xsky[k] = xsky[k]*dx[i] + pos[i, 0]*x_hat[0] + \
                            pos[i, 1]*x_hat[1] + pos[i, 2]*x_hat[2]
                        ysky[k] = ysky[k]*dx[i] + pos[i, 0]*y_hat[0] + \
                            pos[i, 1]*y_hat[1] + pos[i, 2]*y_hat[2]
                        k += 1
                    n += 1
                pbar.update()

    pbar.finish()
    
    return xsky, ysky


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
def pixel_to_cel(np.ndarray[np.float64_t, ndim=1] xsky,
                 np.ndarray[np.float64_t, ndim=1] ysky,
                 np.ndarray[np.float64_t, ndim=1] sky_center):

    cdef int i
    cdef int n = xsky.size
    cdef np.float64_t B, D, cx, cy, sin_cy, cos_cy
    cdef np.float64_t PI = np.pi

    cx = sky_center[0]*PI/180.0
    cy = sky_center[1]*PI/180.0
    sin_cy = sin(cy)
    cos_cy = cos(cy)

    pbar = get_pbar("Converting pixel to celestial coordinates", n)

    for i in range(n):
        
        D = atan(sqrt(xsky[i]*xsky[i] + ysky[i]*ysky[i]))
        B = atan2(-xsky[i], -ysky[i])

        xsky[i] = sin_cy*sin(D)*cos(B) + cos_cy*cos(D)
        ysky[i] = sin(D)*sin(B)

        xsky[i] = cx + atan2(ysky[i], xsky[i])
        ysky[i] = asin(sin_cy*cos(D) - cos_cy*sin(D)*cos(B))

        xsky[i] *= 180.0/PI
        ysky[i] *= 180.0/PI
        
        pbar.update()
        
    pbar.finish()
