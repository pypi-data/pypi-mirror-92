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
from essentia.standard import FrameGenerator
from essentia.standard import Windowing
from essentia.standard import Loudness
from .bark_bands import bark_bands_sone
from .bark_bands import DEFAULT_HOP_SIZE


def loudness(audio, sample_rate, sone=None):
    """ Loudness function from MIRToolbox """
    if sone is None:
        sone = bark_bands_sone(audio, sample_rate)

    frames_count, bands_count = sone.shape

    result = np.zeros(frames_count)
    bands_to_sum = np.ones(bands_count, dtype=bool)
    for i in range(frames_count):
        frame = sone[i, :]
        max_idx = np.argmax(frame)
        peak = sone[i, max_idx]
        bands_to_sum[max_idx] = 0
        result[i] = peak + 0.15 * np.sum(frame, where=bands_to_sum)

    result_t = np.arange(0.5, len(result)) * DEFAULT_HOP_SIZE / sample_rate
    return result_t, result


def essentia_loudness(audio, sample_rate, frame_size=512, hop_size=256):
    get_loudness = Loudness()
    w = Windowing(type='hann', normalized=False, zeroPhase=False)

    frames_count = len(audio) // hop_size
    frames = FrameGenerator(audio, frameSize=frame_size,
                            hopSize=hop_size, startFromZero=True)

    result = np.zeros(frames_count)
    for i, frame in enumerate(frames):
        result[i] = get_loudness(w(frame))

    result_t = np.arange(0.5, len(result)) * hop_size / sample_rate
    return result_t, result
