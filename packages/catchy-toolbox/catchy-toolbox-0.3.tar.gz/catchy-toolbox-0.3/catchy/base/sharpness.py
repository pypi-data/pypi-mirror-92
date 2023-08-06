# 
# MIT License
# 
# Copyright (c) 2020 Music Cognition Group, University of Amsterdam
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import numpy as np
from .bark_bands import bark_bands_sone
from .bark_bands import DEFAULT_HOP_SIZE
from .loudness import loudness as compute_loudness


def sharpness(audio, sample_rate, sone=None, loudness=None):
    if sone is None:
        sone = bark_bands_sone(audio, sample_rate)

    if loudness is None:
        t, loudness = compute_loudness(audio, sample_rate, sone)

    if sone.shape[0] != loudness.shape[0]:
        raise ValueError("Frame number of sone and loudness must be equal")

    z1 = np.arange(1, 16)
    z2 = np.arange(16, 23 + 1)  # TODO: replace 23 with the number of bands?
    Z = np.diag(np.concatenate([z1, z2]))
    g1 = np.full(len(z1), 1)
    g2 = 0.066 * np.exp(0.171 * z2)
    G = np.diag(np.concatenate([g1, g2]))

    shp = 0.22 * np.sum(np.matmul(sone, np.matmul(G, Z)), 1) / loudness
    result_t = np.arange(0.5, len(shp)) * DEFAULT_HOP_SIZE / sample_rate
    return result_t, np.nan_to_num(shp)
