##############################################################################
#
# Copyright (c) 2002-2015 Nexedi SARL and Contributors. All Rights Reserved.
#                    Ivan Tyagov <ivan@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
"""
    Wendelin is a product containing general purpose tools to handle big 
    data manipulations.
"""
from AccessControl import allow_module, allow_type, allow_class

# we neeed to allow access to numpy's internal types
import numpy as np
allow_module('numpy')
for dtype in ('int8', 'int16', 'int32', 'int64', \
              'uint8', 'uint16', 'uint32', 'uint64', \
              'float16', 'float32', 'float64', \
              'complex64', 'complex128',):
  z = np.array([0,], dtype = dtype)
  allow_type(type(z[0]))
  allow_type(type(z))
  
  sz = np.array([(0,)], dtype = [('f0', dtype)])
  allow_type(type(sz[0]))
  allow_type(type(sz))
  
  rz = np.rec.array(np.array([(0,)], dtype = [('f0', dtype)]))
  allow_type(type(rz[0]))
  allow_type(type(rz))

allow_module('sklearn')
allow_module('scipy')

allow_module('wendelin.bigarray.array_zodb')
allow_module('pandas')

allow_type(np.timedelta64)
allow_type(type(np.c_))

import pandas as pd
allow_type(pd.Series)
allow_type(pd.Timestamp)
allow_type(pd.DatetimeIndex)
allow_type(pd.DataFrame)

allow_class(pd.DataFrame)

# Modify 'safetype' dict in full_write_guard function
# of RestrictedPython (closure) directly To allow
# write access to ndarray and ZBigArray objects
from RestrictedPython.Guards import full_write_guard
full_write_guard.func_closure[1].cell_contents.__self__[np.ndarray] = True
full_write_guard.func_closure[1].cell_contents.__self__[np.core.records.recarray] = True
from wendelin.bigarray.array_zodb import ZBigArray
full_write_guard.func_closure[1].cell_contents.__self__[ZBigArray] = True

allow_type(ZBigArray)