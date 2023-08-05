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

from .delegate import delegate

def main_squash():
    'Semi-interactively squash a most-recent chunk of commits.'
    delegate('squash.bash')

def main_drclean():
    'Delete Docker assets.'
    delegate('drclean.bash')

def main_drst():
    'Show Docker assets.'
    delegate('drclean.bash')

def main_examine():
    'Open a shell in a throwaway container of the given image.'
    delegate('examine.bash')

def main_drop():
    'Drop this branch.'
    delegate('drop.bash')

def main_gimports():
    'Stage all imports-only changes and show them.'
    delegate('gimports.bash')

def main_reks():
    'Rebase on a new kitchen-sink branch.'
    delegate('reks.bash')

def main_eb():
    'Rebase on the given branch with completion, or parent with confirmation.'
    delegate('eb.bash')

def main_fixemails():
    'Replace author and committer emails of repo user in history.'
    delegate('fixemails.bash')

def main_mdview():
    'Render Markdown file in browser.'
    delegate('mdview.bash')

def main_vpn():
    'Start openvpn in background.'
    delegate('vpn.bash')

def main_vunzip():
    'Extract a Docker volume.'
    delegate('vunzip.bash')
