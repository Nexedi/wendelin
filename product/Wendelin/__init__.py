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
allow_module('numpy.lib.recfunctions')
for dtype in ('int8', 'int16', 'int32', 'int64', \
              'uint8', 'uint16', 'uint32', 'uint64', \
              'float16', 'float32', 'float64', \
              'complex64', 'complex128'):
  z = np.array([0,], dtype = dtype)
  allow_type(type(z[0]))
  allow_type(type(z))
  
  sz = np.array([(0,)], dtype = [('f0', dtype)])
  allow_type(type(sz[0]))
  allow_type(type(sz))
  
  rz = np.rec.array(np.array([(0,)], dtype = [('f0', dtype)]))
  allow_type(type(rz[0]))
  allow_type(type(rz))

allow_type(np.dtype)
  
sz = np.array([('2017-07-12T12:30:20',)], dtype=[('date', 'M8[s]')])
allow_type(type(sz[0]['date']))

allow_module('sklearn')
allow_module('sklearn.model_selection')
allow_module('sklearn.linear_model')
allow_module('scipy')

allow_module('wendelin.bigarray.array_zodb')
allow_module('pandas')

allow_type(np.timedelta64)
allow_type(type(np.c_))

import pandas as pd
allow_type(pd.Series)
allow_type(pd.Timestamp)
allow_type(pd.DatetimeIndex)
# XXX: pd.DataFRame has its own security thus disable until we can fully integrate it
#allow_type(pd.DataFrame)
allow_type(pd.MultiIndex)
allow_type(pd.Index)
allow_type(pd.core.groupby.DataFrameGroupBy)
allow_class(pd.DataFrame)

import sklearn.linear_model
allow_class(sklearn.linear_model.LinearRegression)

# Modify 'safetype' dict in full_write_guard function
# of RestrictedPython (closure) directly To allow
# write access to ndarray, DataFrame, ZBigArray and RAMArray objects
from RestrictedPython.Guards import full_write_guard
full_write_guard.func_closure[1].cell_contents.__self__[np.ndarray] = True
full_write_guard.func_closure[1].cell_contents.__self__[np.core.records.recarray] = True
full_write_guard.func_closure[1].cell_contents.__self__[np.core.records.record] = True
full_write_guard.func_closure[1].cell_contents.__self__[pd.DataFrame] = True
full_write_guard.func_closure[1].cell_contents.__self__[pd.tseries.index.DatetimeIndex] = True
full_write_guard.func_closure[1].cell_contents.__self__[pd.core.indexing._iLocIndexer] = True
full_write_guard.func_closure[1].cell_contents.__self__[pd.MultiIndex] = True
full_write_guard.func_closure[1].cell_contents.__self__[pd.Index] = True
from wendelin.bigarray.array_zodb import ZBigArray
full_write_guard.func_closure[1].cell_contents.__self__[ZBigArray] = True
allow_type(ZBigArray)
from wendelin.bigarray.array_ram import RAMArray
full_write_guard.func_closure[1].cell_contents.__self__[RAMArray] = True
allow_type(RAMArray)