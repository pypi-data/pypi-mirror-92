# -*- coding: utf-8 -*-

# Copyright 2016 Resonai Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
yabt Build File utils
~~~~~~~~~~~~~~~~~~~~~

:author: Itamar Ostricher
"""


from pathlib import Path
from .config import Config


def to_build_module(build_file_path: str, conf: Config) -> str:
    """Return a normalized build module name for `build_file_path`."""
    build_file = Path(build_file_path)
    root = Path(conf.project_root)
    return build_file.resolve().relative_to(root).parent.as_posix().strip('.')
