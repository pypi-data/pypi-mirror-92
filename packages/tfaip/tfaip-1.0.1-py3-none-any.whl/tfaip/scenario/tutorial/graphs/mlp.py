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
from typing import TYPE_CHECKING

from tensorflow import keras

from tfaip.base.model.components.ff_layer import FF
from tfaip.scenario.tutorial.graphs.tutorialgraph import TutorialGraph

if TYPE_CHECKING:
    from tfaip.scenario.tutorial.model import ModelParams


class MLPLayers(TutorialGraph):
    def __init__(self, params: 'ModelParams', name='MLP', **kwargs):
        super(MLPLayers, self).__init__(params, name=name, **kwargs)
        self.n_classes = params.n_classes
        self.flatten = keras.layers.Flatten()
        self.ff = FF(out_dimension=128, name='f_ff', activation='relu')
        self.logits = FF(out_dimension=params.n_classes, activation=None, name='classify')

    def _call(self, images, **kwargs):
        return self.logits(self.ff(self.flatten(images), **kwargs), **kwargs)
