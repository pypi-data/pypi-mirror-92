import os
import sys

import librosa
import numpy as np

from catchy import utils

""" This module provides an interface to several existing audio feature time
    series extractors.

    Requires Librosa to be installed, and optional Vamp plug-ins.
"""


def compute_and_write(audio_dir, data_dir, features=None):
    """Compute frame-based features for all audio files in a folder.

    Args:
        audio_dir (str): where to find audio files
        data_dir (str): where to write features
        features (dict): dictionary with feature extraction functions, indexed
            by feature name.
            Feature extraction functions should return a time 1d-array of 
            frame times and a 2d-array of feature frames.
            Feature name will be used as the subdirectory to
            which feature CSVs are written.)
        """
    
    if features is None:
        features = {'mfcc': get_mfcc,
                    'hpcp': get_hpcp, 'melody': get_melody,
                    'beats': get_beats,  'onsets': get_onsets}

    filenames = os.listdir(audio_dir)
    for filename in filenames:
        if filename.endswith('.wav') or filename.endswith('.mp3'):
            print("Computing features for file {}...".format(filename))

            x, sr = librosa.load(os.path.join(audio_dir, filename), mono=True)

            for feature in features:
                func = features[feature]
                t, X = func(x, sr)

                track_id = filename.split('.')[-2]
                utils.write_feature([t, X], [data_dir, feature, track_id])


def get_mfcc(x, sr, n_mfcc=20):
    """Compute MFCC features from raw audio, using librosa.
    Librosa must be installed.
    
    Args:
        x (1d-array) audio signal, mono
        sr (int): sample rate
        n_mfcc (int): number of coefficients to retain

    Returns:
        2d-array: MFCC features
    """
    mfcc_all = librosa.feature.mfcc(x, sr)
    n_coeff, n_frames = mfcc_all.shape
    t = librosa.frames_to_time(np.arange(n_frames), sr=sr, hop_length=512)

    return t, mfcc_all[:n_mfcc].T


def get_beats(x, sr):
    """Track beats in an audio excerpt, using librosa's standard
        beat tracker.

    Args:
        x (1d-array) audio signal, mono
        sr (int): sample rate

    Returns:
        2d-array: beat times and beat intervals
    """

    _, beat_frames = librosa.beat.beat_track(x, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    t = beat_times[:-1,]
    beat_intervals = np.diff(beat_times)

    return t, beat_intervals


def get_onsets(x, sr):
    """Compute inter-onset intervals (IOI) from audio, using librosa.

    Args:
        x (1d-array) audio signal, mono
        sr (int): sample rate

    Returns:
        2d-array: onset times and IOI
    """

    onset_frames = librosa.onset.onset_detect(x, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    t = onset_times[:-1,]
    onset_intervals = np.diff(onset_times)

    return t, onset_intervals


if __name__ == '__main__':
    compute_and_write(sys.argv[1], sys.argv[2])
