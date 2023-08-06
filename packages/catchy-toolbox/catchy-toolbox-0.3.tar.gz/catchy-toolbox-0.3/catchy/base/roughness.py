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

import math
import numpy as np
from essentia.standard import Spectrum
from essentia.standard import Windowing
from essentia.standard import FrameGenerator
from .peak_picking import get_essentia_peak_picker
from .peak_picking import get_scipy_peak_picker


FRAME_LENGTH = .05  # Frame length in seconds. Default value from MIRToolbox
HOP_SIZE = .5  # Hopsize relative to the frame length in samples. Default value from MIRToolbox


def roughness(audio, sample_rate, peak_detection='contrast', threshold=0.1, prominence=0.01):
    frame_size = math.floor(sample_rate * FRAME_LENGTH)
    hop_size = math.ceil(sample_rate * FRAME_LENGTH * HOP_SIZE)

    frames = FrameGenerator(audio, frameSize=frame_size,
                            hopSize=hop_size, startFromZero=True)

    spectrum = _get_frames_spectrum(frames)

    if peak_detection == 'essentia':
        peak_picker = get_essentia_peak_picker(threshold, sample_rate)
    elif peak_detection == 'contrast':
        spectrum = list(spectrum)  # Need to gather spectrum frames into list to evaluate max and min
        spec_max = np.max(np.max(spectrum, axis=0))
        spec_min = np.min(np.min(spectrum, axis=0))
        peak_picker = get_scipy_peak_picker(prominence, sample_rate, spec_min, spec_max)
    else:
        raise ValueError("peak_detection argument must be one of ['contrast', 'essentia']")

    result = []
    for s in spectrum:
        freq, mag = peak_picker(s)
        r = _roughness_of_frame(freq, mag)
        result.append(r)

    result_t = np.arange(0.5, len(result)) * hop_size / sample_rate
    return result_t, np.asarray(result)


def _get_frames_spectrum(frames):
    w = Windowing(type='hamming', normalized=False, zeroPhase=False)
    essentia_spectrum = Spectrum()

    for i, frame in enumerate(frames):
        frame_size = len(frame)
        pad = _next_power_of_2(frame_size) - frame_size
        frame_padded = np.pad(w(frame), (0, pad), 'constant')
        yield essentia_spectrum(frame_padded)


def _roughness_of_frame(freq, mag):

    def plomp(f1, f2):
        b1 = 3.51
        b2 = 5.75
        xstar = .24
        s1 = .0207
        s2 = 18.96

        s = np.tril(np.divide(xstar, (s1 * np.fmin(f1, f2) + s2)))
        return np.exp(-b1 * s * np.abs(f2 - f1)) - np.exp(-b2 * s * np.abs(f2 - f1))

    f1 = np.tile(np.atleast_2d(freq).T, (1, len(freq)))
    f2 = np.tile(np.atleast_2d(freq), (len(freq), 1))
    v1 = np.tile(np.atleast_2d(mag).T, (1, len(freq)))
    v2 = np.tile(np.atleast_2d(mag), (len(freq), 1))
    rj = plomp(f1, f2)

    v12 = v1 * v2
    rj = v12 * rj

    return np.sum(np.sum(rj))


def _next_power_of_2(x):
    return 1 << (x-1).bit_length()
