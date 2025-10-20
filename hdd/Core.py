#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
#
# Author: Metaer @ 2025/10/18
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
from pathlib import Path
from .service import Core


aliases = {
    "config": "hdd.service.config.ConfigManager",
    "pipeline": "hdd.service.pipeline.Pipeline",
    # "db": "hdd.interface.abs.DBManagerAbs",
    # "DB": "hdd.interface.abs.DBManagerAbs",
}


try:
    package_absolute_path = Path(__file__).absolute().parent
    project_absolute_path = Path.cwd()

    sys.path.append(str(project_absolute_path))
except:
    pass

core = Core(package_absolute_path, project_absolute_path, aliases)

config = core.make("config")

core.bootstrap(config.get("bootstrappers"))
