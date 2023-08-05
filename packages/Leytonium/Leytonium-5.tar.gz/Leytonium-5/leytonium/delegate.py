# Copyright 2020 Andrzej Cichocki

# This file is part of Leytonium.
#
# Leytonium is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Leytonium is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Leytonium.  If not, see <http://www.gnu.org/licenses/>.

from lagoon import bash
from pathlib import Path
import inspect, sys

class Interpreter:

    def bash(path):
        with path.open('rb') as f:
            text = f.read()
        bash._c[exec](text, *sys.argv)

def delegate(*relpath):
    path = Path(Path(inspect.stack()[1].filename).parent, *relpath)
    name = path.name
    getattr(Interpreter, name[name.rindex('.') + 1:])(path)
