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
import pandas as pd

from .utils import read_feature
from .high.feature_transforms import parse_feature
from .high.feature_transforms import first_order
from .high.feature_transforms import second_order


def process_high_features(data_dir, segment_dict, features):
    return _compute(segment_dict, features, data_dir)


def _compute(segment_dict, features, data_dir):
    """
    Args:
        segment_dict (dict): dictionary of song segments, containing a list of
            segment ids (values) for a set of unique song identifiers (keys).
    """

    data_dict = {}

    # compute features
    for feature in features:
        print('computing ' + feature + '...')
        feature_name, first_order_aggregates, second_order_aggregates = parse_feature(feature)

        corpus_features = []
        for song_id in segment_dict.keys():
            song_features = []
            for segment in segment_dict[song_id]:
                raw_features = read_feature([data_dir, feature_name, segment], skip_cols='auto')
                segment_features = first_order(raw_features, first_order_aggregates, verbose=False)
                song_features.append(segment_features)
            if 'song' in second_order_aggregates:
                song_features = second_order(song_features, second_order_aggregates, verbose=False)
            corpus_features.extend(song_features)
        if 'corpus' in second_order_aggregates:
            # print('        in: len(corpus_features) = {}, corpus_features[0] = {}'.format(len(corpus_features), corpus_features[0]))
            corpus_features = second_order(corpus_features, second_order_aggregates, verbose=False)
        # print('        out: len(corpus_features) = {}, corpus_features[0] = {}'.format(len(corpus_features), corpus_features[0]))
        data_dict[feature] = np.squeeze(corpus_features)

    # add segment ids
    song_ids = []
    segments = []
    for song_id in segment_dict.keys():
        for segment in segment_dict[song_id]:
            song_ids.append(song_id)
            segments.append(segment)
    data_dict['song.id'] = np.array(song_ids)
    data_dict['segment.id'] = np.array(segments)

    # convert to dataframe
    return pd.DataFrame(data_dict)
