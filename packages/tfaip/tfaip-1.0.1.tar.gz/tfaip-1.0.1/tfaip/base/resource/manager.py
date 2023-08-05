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
import shutil
from dataclasses import fields
from typing import Dict, Optional
import os
import logging

from tfaip.base.resource.resource import Resource


logger = logging.getLogger(__name__)


class ResourceManager:
    def __init__(self, working_dir: str, dump_prefix_dir: str = 'resources'):
        self.working_dir = working_dir if working_dir is not None else os.getcwd()
        self.dump_prefix_dir = dump_prefix_dir
        self._resources: Dict[str, Resource] = {}

    def register_all(self, params):
        for field in fields(params):
            value = getattr(params, field.name)
            if value is None:
                continue

            if isinstance(value, Resource):
                self.register(field.name, value)
            elif isinstance(value, str) and (field.type == Resource or field.type == Optional[Resource]):
                self.register(field.name, Resource(value))

    def register(self, r_id: str, resource: Resource):
        if r_id in self._resources:
            raise KeyError(f"A resource with id {r_id} already exists.")

        if not resource.initialized:
            if resource.abs_path is None:
                resource.abs_path = os.path.abspath(os.path.join(self.working_dir, resource.rel_path))

            resource.basename = os.path.basename(resource.rel_path)
            resource.dump_path = os.path.join(self.dump_prefix_dir, resource.dump_dir, resource.basename)

        resource.initialized = True
        self._resources[r_id] = resource
        return resource

    def items(self):
        return self._resources.items()

    def __contains__(self, item: str):
        return item in self._resources

    def get(self, resource_id: str) -> Resource:
        return self._resources[resource_id]

    def dump(self, location: str):
        for r_id, resource in self._resources.items():
            dump_dir = os.path.join(location, self.dump_prefix_dir, resource.dump_dir)
            abs_dump_path = os.path.join(location, resource.dump_path)
            logger.debug(f"Exporting resource {r_id} to {dump_dir}")
            os.makedirs(dump_dir, exist_ok=True)
            shutil.copy(resource.abs_path, abs_dump_path)
