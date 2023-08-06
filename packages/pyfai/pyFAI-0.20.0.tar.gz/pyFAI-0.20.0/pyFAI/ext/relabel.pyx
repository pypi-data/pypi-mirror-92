# -*- coding: utf-8 -*-
#cython: embedsignature=True, language_level=3
#cython: boundscheck=False, wraparound=False, cdivision=True, initializedcheck=False,
## This is for developping
## cython: profile=True, warn.undeclared=True, warn.unused=True, warn.unused_result=False, warn.unused_arg=True
# -*- coding: utf-8 -*-
#
#    Project: Fast Azimuthal integration
#             https://github.com/silx-kit/pyFAI
#
#    Copyright (C) 2012-2020 European Synchrotron Radiation Facility, France
#
#    Principal author:       Jérôme Kieffer (Jerome.Kieffer@ESRF.eu)
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#  .
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#  .
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

"""Module providing features to relabel regions.

It is used to flag from largest regions to the smallest.
"""

__author__ = "Jerome Kieffer"
__contact__ = "Jerome.kieffer@esrf.fr"
__date__ = "14/01/2021"
__status__ = "stable"
__license__ = "MIT"

import numpy
from libc.stdint cimport int8_t, uint8_t, int16_t, uint16_t, \
                         int32_t, uint32_t, int64_t, uint64_t

ctypedef double float64_t
ctypedef float float32_t

def countThem(label,
              data,
              blured):
    """Count

    :param label: 2D array containing labeled zones
    :param data: 2D array containing the raw data
    :param blured: 2D array containing the blured data
    :return: 2D arrays containing:

        * count pixels in labeled zone: label == index).sum()
        * max of data in that zone:      data[label == index].max()
        * max of blurred in that zone:    blured[label == index].max()
        * data-blurred where data is max.
    """
    cdef:
        uint32_t[::1] clabel = numpy.ascontiguousarray(label.ravel(), dtype=numpy.uint32)
        float[::1] cdata = numpy.ascontiguousarray(data.ravel(), dtype=numpy.float32)
        float[::1] cblured = numpy.ascontiguousarray(blured.ravel(), dtype=numpy.float32)
        size_t maxLabel = label.max()
        uint64_t[::1] count = numpy.zeros(maxLabel + 1, dtype=numpy.uint64)
        float32_t[::1] maxData = numpy.zeros(maxLabel + 1, dtype=numpy.float32)
        float32_t[::1] maxBlured = numpy.zeros(maxLabel + 1, dtype=numpy.float32)
        float32_t[::1] maxDelta = numpy.zeros(maxLabel + 1, dtype=numpy.float32)
        int s, i, idx
        float d, b
    s = label.size
    assert s == cdata.size, "cdata.size"
    assert s == cblured.size, "cblured.size"
    with nogil:
        for i in range(s):
            idx = clabel[i]
            d = cdata[i]
            b = cblured[i]
            count[idx] += 1
            if d > maxData[idx]:
                maxData[idx] = d
                maxDelta[idx] = d - b
            if b > maxBlured[idx]:
                maxBlured[idx] = b
    return numpy.asarray(count), numpy.asarray(maxData), numpy.asarray(maxBlured), numpy.asarray(maxDelta)
