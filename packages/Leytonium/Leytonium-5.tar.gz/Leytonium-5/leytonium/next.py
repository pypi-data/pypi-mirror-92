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

from lagoon import git
from pathlib import Path

def main_next():
    'Go to next step in current git workflow.'
    gitdir = Path(git.rev_parse.__git_dir().rstrip())
    if (gitdir / 'rebase-apply').is_dir():
        if git.status.__porcelain().splitlines():
            git[print].rebase.__continue()
        else:
            git[print].rebase.__skip()
    elif (gitdir / 'MERGE_HEAD').is_file():
        git[print].commit.__no_edit()
    elif (gitdir / 'CHERRY_PICK_HEAD').is_file():
        git[print].cherry_pick.__continue()
    elif (gitdir / 'REVERT_HEAD').is_file():
        git[print].revert.__continue()
    else:
        raise Exception('Unknown git workflow, giving up.')
