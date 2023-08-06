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
from essentia.standard import PeakDetection
from scipy.signal import find_peaks


def get_essentia_peak_picker(threshold, sample_rate):
    return PeakDetection(threshold=threshold, range=sample_rate // 2,
                         interpolate=True, maxPosition=sample_rate // 2,
                         minPosition=0)


def get_scipy_peak_picker(prominence, sample_rate, spec_min, spec_max):

    def rescale_frequencies(freq, sr, spec_size):
        freq_scale = sr / 2 * np.linspace(0, 1, spec_size)
        f_scaled = np.zeros(len(freq))
        for i, f in np.ndenumerate(freq):
            f_scaled[i] = freq_scale[f]

        return f_scaled

    def pick(spectrum):
        spectrum_normalized = (spectrum - spec_min) / (spec_max - spec_min)
        x_freq, props = find_peaks(spectrum_normalized, prominence=(prominence, None))
        freq = rescale_frequencies(x_freq, sample_rate, len(spectrum))
        return freq, (spectrum[x_freq])

    return lambda spectrum: pick(spectrum)
