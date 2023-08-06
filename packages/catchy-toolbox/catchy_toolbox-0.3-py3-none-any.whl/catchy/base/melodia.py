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
from essentia.streaming import PredominantPitchMelodia
from essentia.streaming import VectorInput

DEFAULT_FRAME_SIZE = 1024
DEFAULT_HOP_SIZE = 64


def melodia(audio, sample_rate):
    audio_input = VectorInput(audio)
    pitch_melodia = PredominantPitchMelodia(sampleRate=sample_rate, frameSize=DEFAULT_FRAME_SIZE,
                                            hopSize=DEFAULT_HOP_SIZE, guessUnvoiced=False, minFrequency=55,
                                            maxFrequency=1760, binResolution=10, peakFrameThreshold=0.9)
    out_pool = essentia.Pool()

    audio_input.data >> pitch_melodia.signal
    pitch_melodia.pitch >> (out_pool, 'melodia')
    pitch_melodia.pitchConfidence >> (out_pool, 'melodiaConfidence')

    essentia.run(audio_input)

    result_t = np.arange(0.5, len(out_pool['melodia'])) * DEFAULT_HOP_SIZE / sample_rate
    return result_t, out_pool['melodia']
