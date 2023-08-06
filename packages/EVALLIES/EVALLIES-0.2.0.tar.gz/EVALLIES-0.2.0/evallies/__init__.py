# -* coding: utf-8 -*-
#
# This file is part of EVALLIES.
#
# EVALLIES is a python package for lifelong learning speaker diarization.
# Home page: https://git-lium.univ-lemans.fr/Larcher/evallies
#
# EVALLIES is free software: you can redistribute it and/or modify
# it under the terms of the GNU LLesser General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# EVALLIES is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with SIDEKIT.  If not, see <http://www.gnu.org/licenses/>.
"""
Copyright 2020-2021 Anthony Larcher

    :mod:`init`

"""


from .database import Database

from .user_simulation import UserSimulation
from .user_simulation import MessageToUser 
from .user_simulation import Request

from .der_single import der_single_averaged
from .der_run import der_incremental
from .der_cross import der_cross
from .der_cross import der_cross_across_time

#from .lium_baseline.system import allies_load_seg
from .lium_baseline.system import allies_initial_training
from .lium_baseline.system import lium_iv_initial_training
from .lium_baseline.system import lium_xv_initial_training
from .lium_baseline.system import extract_vectors
from .lium_baseline.system import allies_init_seg
from .lium_baseline.system import allies_within_show_HAL
from .lium_baseline.system import allies_cross_show_clustering
from .lium_baseline.system import allies_write_diar

from .lium_baseline.interactive import apply_correction
from .lium_baseline.interactive import apply_correction_min
from .lium_baseline.interactive import apply_correction_max
from .lium_baseline.interactive import apply_correction_avr

__author__ = "Anthony Larcher"
__copyright__ = "Copyright 2020-2021 Anthony Larcher"
__license__ = "LGPL"
__maintainer__ = "Anthony Larcher"
__email__ = "anthony.larcher@univ-lemans.fr"
__status__ = "Production"
__docformat__ = 'reStructuredText'
__version__="0.2.0"
