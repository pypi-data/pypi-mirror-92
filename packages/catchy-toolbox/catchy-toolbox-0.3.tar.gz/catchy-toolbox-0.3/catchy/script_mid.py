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

import os
import numpy as np

from .utils import write_feature

from .mid.pitch_features import set_feature_dirs
from .mid.pitch_features import get_pitchhist
from .mid.pitch_features import get_pitchhist2
from .mid.pitch_features import get_pitchhist3
from .mid.pitch_features import get_chromahist2
from .mid.pitch_features import get_chromahist3
from .mid.pitch_features import get_harmonisation

from .mid.rhythm_features import set_input_dirs
from .mid.rhythm_features import local_tempo
from .mid.rhythm_features import log_ioi
from .mid.rhythm_features import ioi_histogram
from .mid.rhythm_features import raw_pvi
from .mid.rhythm_features import norm_pvi


def process_pitch_features(input_dir, output_dir, track_list=None, features=None):
    _compute_and_write_pitch(input_dir, data_dir=output_dir, track_list=track_list, features=features)


def process_rhythm_features(input_dir, output_dir, track_list=None, features=None):
    _compute_and_write_rhythm(input_dir, output_dir, track_list, features)


def _compute_and_write_pitch(input_dir, data_dir, track_list=None, features=None):
    """Compute frame-based features for all audio files in a folder.

    Args:
        input_dir (str): directory path with chroma and melody features
        data_dir (str): where to write features
        track_list (str or None): list of file ids. Set to None to infer from
            files in melody_dir and chroma_dir (the intersection is used).
        features (dict): dictionary with (unique) feature names as keys and
            tuples as values, each containing a feature extraction function and a
            parameter dictionary.
            Feature extraction functions can be any function that returns one
                or more 1d or 2d-arrays that share their first dimension.

    Required global variables:
        melody_dir (str): where to find melody data
        chroma_dir (str): where to find chroma data
    """

    melody_dir = os.path.join(input_dir, 'melody/')
    chroma_dir = os.path.join(input_dir, 'hpcp/')
    set_feature_dirs(melody_dir, chroma_dir)

    if track_list is None:
        melody_ids = [filename.split('.')[0] for filename in os.listdir(melody_dir)]
        chroma_ids = [filename.split('.')[0] for filename in os.listdir(chroma_dir)]

        track_list = list(set(melody_ids + chroma_ids))

    if features is None:
        features = {'pitchhist': (get_pitchhist, {}),
                    'pitchhist2': (get_pitchhist2, {}),
                    'pitchhist3': (get_pitchhist3, {}),
                    'pitchhist3_int': (get_pitchhist3, {'intervals': True, 'diagfactor': 1, 'sqrt': False}),
                    # 'chromahist2': (get_chromahist2, {}),
                    # 'chromahist3': (get_chromahist3, {}),
                    # 'chromahist3_int': (get_chromahist3, {'intervals': True}),
                    # 'harmonisation': (get_harmonisation, {}),
                    # 'harmonisation_int': (get_harmonisation, {'intervals': True})
                    }

    for track_id in track_list:

        print("Computing features for track {}...".format(track_id))

        for feature in features:
            # run feature function
            func, params = features[feature]
            X = func(track_id, **params)

            # normalize (!) and flatten
            X = X.flatten() / np.sum(X)

            # write
            write_feature(X, [data_dir, feature, track_id])


def _compute_and_write_rhythm(input_dir, data_dir, track_list=None, features=None):
    """Compute frame-based features for all audio files in a folder.

    Args:
        input_dir (str): directory path with onsets and beats features
        data_dir (str): where to write features
        track_list (str or None): list of file ids. Set to None to infer from
            files in beats_dir and onsets_dir.
        features (dict): dictionary with (unique) feature names as keys and
            tuples as values, each containing a feature extraction function and a
            parameter dictionary.
            Feature extraction functions can be any function that returns one
                or more 1d or 2d-arrays that share their first dimension.

    Required global variables:
        beats_dir (str): where to find beat data
        onsets_dir (str): where to find onset data
    """

    onsets_dir = os.path.join(input_dir, 'onsets/')
    beats_dir = os.path.join(input_dir, 'beats/')

    set_input_dirs(onsets_dir, beats_dir)

    if track_list is None:
        onsets_ids = [filename.split('.')[0] for filename in os.listdir(onsets_dir)]
        beats_ids = [filename.split('.')[0] for filename in os.listdir(beats_dir)]

        track_list = list(set(onsets_ids + beats_ids))

    if features is None:
        features = {'tempo': (local_tempo, {}),
                    'log_norm_ioi': (log_ioi, {'normalize_ioi': True}),
                    'log_norm_ioi_hist': (ioi_histogram, {'min_length': -3, 'max_length': 3, 'step': 0.5}),
                    'rpvi': (raw_pvi, {'normalize_ioi': False}),
                    'npvi': (norm_pvi, {'normalize_ioi': False})}

    for track_id in track_list:

        print("Computing features for track {}...".format(track_id))

        for feature in features:

            # run feature function
            func, params = features[feature]
            X = func(track_id, **params)

            # flatten
            X = X.flatten()

            # write
            write_feature(X, [data_dir, feature, track_id])
