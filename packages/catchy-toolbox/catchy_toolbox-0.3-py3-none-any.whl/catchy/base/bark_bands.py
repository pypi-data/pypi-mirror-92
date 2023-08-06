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
from essentia.standard import FFT

DEFAULT_FRAME_SIZE = 512
DEFAULT_HOP_SIZE = 256
BARK_BANDS = [100, 200, 300, 400, 510, 630, 770, 920, 1080, 1270, 1480, 1720,
              2000, 2320, 2700, 3150, 3700, 4400, 5300, 6400, 7700, 9500, 12000]


def bark_bands_sone(audio, sample_rate):
    bands_count = len(BARK_BANDS)  # TODO: It should be calculated

    frames_number = len(audio) // DEFAULT_HOP_SIZE
    sone = np.zeros((bands_count, frames_number))
    frames = FrameGenerator(audio, frameSize=DEFAULT_FRAME_SIZE,
                            hopSize=DEFAULT_HOP_SIZE, startFromZero=True)

    for i, frame in enumerate(frames):
        sone[:, i] = _bark_bands_of_frame(frame, sample_rate, bands_count)

    sone = _spread_masking(sone, bands_count)
    sone = _log_scale(sone)
    sone = _vowels_model(sone)

    return sone.T


def _bark_bands_of_frame(frame, sample_rate, bands_count):
    fft = FFT()
    w = Windowing(type='hann', normalized=False, zeroPhase=False)

    # Normalization factor from the MIRToolbox.
    # rescale to dB max (default is 96dB = 2^16)
    # 96dB is the default value of the max_dB parameter.
    normalize_factor = 10 ** (96 / 20)
    normalized = frame * normalize_factor

    spectrum_raw = fft(w(normalized))

    # Normalized power spectrum. Linear frequency scale
    hamming_window_sum = np.sum(w(np.full(len(frame), 1)))
    spectrum = abs(spectrum_raw / hamming_window_sum * 2) ** 2

    outer_ear_spectrum = _terhardt(frame, spectrum, sample_rate)
    return _group_into_bark_bands(frame, outer_ear_spectrum, sample_rate, bands_count)


def _terhardt(frame, spectrum, sample_rate):
    """ Model of outer ear. terhardt 1979 (calculating virtual pitch,
    hearing research #1, pp 155-182)
    """

    fft_size = len(frame)
    spec_size = len(spectrum)

    # FFT bins frequency
    fft_bf = (np.arange(0, spec_size)) / fft_size * 2 * (sample_rate / 2)

    adb_weights = np.zeros(spec_size)
    adb_weights[0] = 0
    adb_weights[1:spec_size] = -3.64 * (fft_bf[1:spec_size] / 1000) ** -0.8 \
                               + 6.5 * np.exp(-0.6 * (fft_bf[1:spec_size] / 1000 - 3.3) ** 2) \
                               - 0.001 * (fft_bf[1:spec_size] / 1000) ** 4
    adb_weights[1:spec_size] = (10 ** (adb_weights[1:spec_size] / 20)) ** 2

    return spectrum * adb_weights


def _group_into_bark_bands(frame, spectrum, sample_rate, bands_count):
    fft_size = len(frame)
    spec_size = len(spectrum)

    # FFT bins frequency
    fft_bf = (np.arange(0, spec_size)) / fft_size * 2 * (sample_rate / 2)

    sone = np.zeros(bands_count)

    b_idx = 0
    f_idx = 0
    while b_idx < bands_count:
        while f_idx < spec_size and fft_bf[f_idx] <= BARK_BANDS[b_idx]:
            sone[b_idx] += spectrum[f_idx]
            f_idx += 1
        b_idx += 1

    return sone


def _spread_masking(sone, bands_count):
    spread = np.zeros((bands_count, bands_count))
    for i in range(bands_count):
        spread[i, :] = 10 ** ((15.81 + 7.5 * ((i - np.arange(0, bands_count)) + 0.474) \
                               - 17.5 * (1 + ((i - np.arange(0, bands_count)) + 0.474) ** 2) ** 0.5) / 10)

    return np.matmul(spread, sone)


def _log_scale(sone):
    r = np.where(sone < 1, 1, sone)
    return 10 * np.log10(r)


def _vowels_model(sone):
    """ bladon and lindblom, 1981, JASA,
    modelling the judment of vowel quality differences """
    return np.where(sone >= 40, 2 ** ((sone - 40) / 10), (sone / 40) ** 2.642)
