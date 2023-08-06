# -*- coding: utf-8 -*-
#cython: embedsignature=True, language_level=3
#cython: boundscheck=False, wraparound=False, cdivision=True, initializedcheck=False,
## This is for developping:
##cython: profile=True, warn.undeclared=True, warn.unused=True, warn.unused_result=False, warn.unused_arg=True
#
#    Project: Fast Azimuthal Integration
#             https://github.com/silx-kit/pyFAI
#
#    Copyright (C) 2014-2021 European Synchrotron Radiation Facility, Grenoble, France
#
#    Principal author:   Pierre Paleo <pierre.paleo@gmail.com>
#                        Jérôme Kieffer (Jerome.Kieffer@ESRF.eu)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Implementation of a separable 2D convolution.

It is used in real space are used to blurs images, used in blob-detection
algorithm.
"""

__authors__ = ["Pierre Paleo", "Jérôme Kieffer"]
__contact__ = "Jerome.kieffer@esrf.fr"
__date__ = "11/01/2021"
__status__ = "stable"
__license__ = "MIT"

import cython
import numpy
from cython.parallel import prange


def horizontal_convolution(float[:, ::1] img, 
                           float[::1] filter):
    """
    Implements a 1D horizontal convolution with a filter.
    The only implemented mode is "reflect" (default in scipy.ndimage.filter)

    Use Mixed precision accumulator

    :param img: input image
    :param filter: 1D array with the coefficients of the array
    :return: array of the same shape as image with
    """
    cdef:
        int FILTER_SIZE, HALF_FILTER_SIZE
        int IMAGE_H, IMAGE_W
        int x, y, fIndex, newpos
        double acc
        float[:, ::1] output

    FILTER_SIZE = filter.shape[0]
    if FILTER_SIZE % 2 == 1:
        HALF_FILTER_SIZE = (FILTER_SIZE) // 2
    else:
        HALF_FILTER_SIZE = (FILTER_SIZE + 1) // 2

    IMAGE_H = img.shape[0]
    IMAGE_W = img.shape[1]
    output = numpy.zeros((IMAGE_H, IMAGE_W), dtype=numpy.float32)
    for y in prange(IMAGE_H, nogil=True):
        for x in range(IMAGE_W):
            acc = 0.0
            for fIndex in range(FILTER_SIZE):
                newpos = x + fIndex - HALF_FILTER_SIZE
                if newpos < 0:
                    newpos = - newpos - 1
                elif newpos >= IMAGE_W:
                    newpos = 2 * IMAGE_W - newpos - 1
                acc += img[y, newpos] * filter[fIndex]
            output[y, x] += <float> acc
    return numpy.asarray(output)


def vertical_convolution(float[:, ::1] img, float[::1] filter):
    """
    Implements a 1D vertical convolution with a filter.
    The only implemented mode is "reflect" (default in scipy.ndimage.filter)

    Use Mixed precision accumulator

    :param img: input image
    :param filter: 1D array with the coefficients of the array
    :return: array of the same shape as image with
    """
    cdef:
        int FILTER_SIZE, HALF_FILTER_SIZE
        int IMAGE_H, IMAGE_W
        int x, y, fIndex, newpos
        double acc
        float[:, ::1] output

    FILTER_SIZE = filter.shape[0]
    if FILTER_SIZE % 2 == 1:
        HALF_FILTER_SIZE = (FILTER_SIZE) // 2
    else:
        HALF_FILTER_SIZE = (FILTER_SIZE + 1) // 2

    IMAGE_H = img.shape[0]
    IMAGE_W = img.shape[1]
    output = numpy.zeros((IMAGE_H, IMAGE_W), dtype=numpy.float32)
    for y in prange(IMAGE_H, nogil=True):
        for x in range(IMAGE_W):
            acc = 0.0
            for fIndex in range(FILTER_SIZE):
                newpos = y + fIndex - HALF_FILTER_SIZE
                if newpos < 0:
                    newpos = - newpos - 1
                elif newpos >= IMAGE_H:
                    newpos = 2 * IMAGE_H - newpos - 1
                acc += img[newpos, x] * filter[fIndex]
            output[y, x] += <float> acc
    return numpy.asarray(output)


def gaussian(sigma, width=None):
    """
    Return a Gaussian window of length "width" with standard-deviation "sigma".

    :param sigma: standard deviation sigma
    :param width: length of the windows (int) By default 8*sigma+1,

    Width should be odd.

    The FWHM is 2*sqrt(2 * pi)*sigma

    """
    if width is None:
        width = int(8 * sigma + 1)
        if width % 2 == 0:
            width += 1
    sigma = float(sigma)
    x = numpy.arange(width) - (width - 1) / 2.0
    g = numpy.exp(-(x / sigma) ** 2 / 2.0)
    #  Normalization is done at the end to cope for numerical precision
    return g / g.sum()


def gaussian_filter(img, sigma):
    """
    Performs a gaussian bluring using a gaussian kernel.

    :param img: input image
    :param sigma: width parameter of the gaussian
    """
    raw = numpy.ascontiguousarray(img, dtype=numpy.float32)
    gauss = gaussian(sigma).astype(numpy.float32)
    res = vertical_convolution(horizontal_convolution(raw, gauss), gauss)
    return res
