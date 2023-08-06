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

import essentia
import numpy as np
from essentia.streaming import FrameCutter
from essentia.streaming import HPCP
from essentia.streaming import SpectralPeaks
from essentia.streaming import Spectrum
from essentia.streaming import VectorInput
from essentia.streaming import Windowing

FRAME_LENGTH = 1024  # Frame length in seconds. Default value from MIRToolbox
HOP_SIZE = 256  # Hopsize relative to the frame length in samples. Default value from MIRToolbox


def hpcp(audio, sample_rate):
    audio_input = VectorInput(audio)

    fc = FrameCutter(frameSize=FRAME_LENGTH, hopSize=HOP_SIZE, silentFrames='noise')
    w = Windowing(type='blackmanharris62', zeroPadding=0, normalized=True)
    spec = Spectrum()

    peaks = SpectralPeaks(maxPeaks=60, magnitudeThreshold=0.00001,
                          minFrequency=20.0, maxFrequency=3500.0,
                          orderBy='magnitude')

    hpcp = HPCP(size=12, referenceFrequency=440.0, bandPreset=False,
                minFrequency=20.0, maxFrequency=3500.0, weightType='cosine',
                nonLinear=False, windowSize=1.0, sampleRate=sample_rate)

    pool = essentia.Pool()

    audio_input.data >> fc.signal
    fc.frame >> w.frame
    w.frame >> spec.frame
    spec.spectrum >> peaks.spectrum
    peaks.frequencies >> hpcp.frequencies
    peaks.magnitudes >> hpcp.magnitudes
    hpcp.hpcp >> (pool, 'hpcp')

    essentia.run(audio_input)

    result_t = np.arange(0.5, len(pool['hpcp'])) * HOP_SIZE / sample_rate
    return result_t, pool['hpcp']
