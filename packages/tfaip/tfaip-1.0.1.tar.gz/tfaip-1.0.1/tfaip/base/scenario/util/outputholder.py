# Copyright 2020 The tfaip authors. All Rights Reserved.
#
# This file is part of tfaip.
#
# tfaip is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# tfaip is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# tfaip. If not, see http://www.gnu.org/licenses/.
# ==============================================================================
import tensorflow.keras as keras
import tensorflow as tf
import numpy as np


class OutputHolderMetricWrapper(keras.metrics.Metric):
    """
    Metric that holds the outputs of the last batch.

    Used to write this data to the logs, which can then be written to the tensorboard
    """
    def __init__(self, input_shape, dtype, n_storage=2, **kwargs):
        super(OutputHolderMetricWrapper, self).__init__(**kwargs)
        initial_value = np.zeros([0 if s is None else s for s in input_shape])
        self.store_w = tf.Variable(initial_value=initial_value, shape=input_shape, trainable=False, validate_shape=False, name=f'store', dtype=dtype)
        self.n_storage = n_storage

    def update_state(self, y_true, y_pred, **kwargs):
        return self.store_w.assign(y_pred)

    def result(self):
        return tf.stack(self.store_w)

    def reset_states(self):
        self.store_w.assign_sub(self.store_w)
