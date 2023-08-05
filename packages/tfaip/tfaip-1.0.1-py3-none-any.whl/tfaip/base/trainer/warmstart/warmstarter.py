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
from typing import List, Optional

from tfaip.base.trainer.warmstart.warmstart_params import WarmstartParams
import tensorflow as tf
import logging
import re


logger = logging.getLogger(__name__)


def longest_common_startstr(strs: List[str]):
    longest_common = ''
    for c in zip(*strs):
        if len(set(c)) == 1:
            longest_common += c[0]
        else:
            break

    return longest_common


class Warmstarter:
    def __init__(self, params: WarmstartParams):
        self._params = params

        if (params.exclude or params.include) and params.allow_partial:
            raise ValueError("Allow partial is only allowed if neither exclude not include is specified")

    def _trim(self, names: List[str]) -> List[str]:
        if self._params.trim_graph_name:
            longest_common = longest_common_startstr([n for n in names if 'print_limit' not in n])
            if '/' in longest_common:
                # find slash, only trim full var names
                longest_common = longest_common[:longest_common.rfind('/') + 1]
                return [s[len(longest_common):] if 'print_limit' not in s else s for s in names]
        return names

    @staticmethod
    def _replace_name(name, rename_rules: Optional[List[str]] = None):
        if rename_rules:
            for replace in rename_rules:
                from_to = replace.split('->')
                if len(from_to) != 2:
                    raise ValueError(f"Renaming rule {replace} must follow the 'from->to' schemata")

                name = name.replace(from_to[0], from_to[1])

        return name

    def _apply_renamings(self, names, rename_params: Optional[List[str]]):
        names = self._trim(names)
        if rename_params:
            names = [self._replace_name(n, rename_params) for n in names]
        names = [self._auto_replace_numbers(n) for n in names]
        return names

    def _auto_replace_numbers(self, name):
        for r in self._params.auto_remove_numbers_for:
            name = re.sub(f"(.*/){r}_\\d+(/.*)", f"\\1{r}\\2", name)

        return name

    def warmstart(self, target_model: tf.keras.Model, custom_objects=None):
        if not self._params.model:
            logger.debug("No warm start model provided")
            return

        target_var_names = self._apply_renamings([w.name for w in target_model.weights], self._params.rename_targets)
        target_weights = list(zip(target_var_names, target_model.weights, target_model.get_weights()))
        all_trainable_target_weights = {name: weight for name, var, weight in target_weights if var.trainable}
        all_target_weights = {name: weight for name, var, weight in target_weights}
        logger.info(f"Warmstarting from {self._params.model}")
        try:
            model = tf.keras.models.load_model(self._params.model, compile=False, custom_objects=custom_objects)
            loaded_var_names = self._apply_renamings([w.name for w in model.weights], self._params.rename)
            loaded_weights = list(zip(loaded_var_names, model.weights, model.get_weights()))
            all_loaded_weights = {name: weight for name, var, weight in loaded_weights if var.trainable}
        except OSError:
            logger.debug(f"Could not load '{self._params.model}' as saved model. Attempting to load as a checkpoint.")
            ckpt = tf.train.load_checkpoint(self._params.model)
            name_shapes = ckpt.get_variable_to_shape_map()
            var_names_ckpt = name_shapes.keys()

            def rename_ckpt_var_name(name: str):
                name = name.rstrip('/.ATTRIBUTES/VARIABLE_VALUE')
                return name
            names = self._apply_renamings(var_names_ckpt, self._params.rename)
            weights_ckpt = {rename_ckpt_var_name(pp_name): ckpt.get_tensor(name) for pp_name, name in zip(names, var_names_ckpt)}
            all_loaded_weights = weights_ckpt

        names_target = set(all_trainable_target_weights.keys())
        names_loaded = set(all_loaded_weights.keys())
        if self._params.exclude or self._params.include:
            names_to_load = names_loaded
            if self._params.include:
                inc = re.compile(self._params.include)
                names_to_load = [name for name in names_to_load if inc.fullmatch(name)]

            if self._params.exclude:
                exc = re.compile(self._params.exclude)
                names_to_load = [name for name in names_to_load if not exc.fullmatch(name)]

            if len(names_target.intersection(names_to_load)) == 0:
                raise NameError(f"Not a weight could be matched.\nLoaded: {names_to_load}\nTarget: {names_target}")
        elif self._params.allow_partial:
            names_to_load = names_target.intersection(names_loaded)
        else:
            diff_target = names_loaded.difference(names_target)
            diff_load = names_target.difference(names_loaded)
            if len(diff_target) > 0 or len(diff_load) > 0:
                raise NameError(f"Not all weights could be matched:\nTargets '{diff_target}'\nLoaded: '{diff_load}'. "
                                f"\nUse allow_partial to allow partial loading")

            names_to_load = names_target

        new_weights = [all_loaded_weights[name] if name in names_to_load else all_target_weights[name] for name in target_var_names]
        self.apply_weights(target_model, new_weights)
        logger.info(f"Warmstarted weights: {names_to_load}")

    def apply_weights(self, target_model, new_weights):
        target_model.set_weights(new_weights)
