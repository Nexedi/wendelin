##############################################################################
#
# Copyright (c) 2002-2015 Nexedi SA and Contributors. All Rights Reserved.
#                    Ivan Tyagov <ivan@nexedi.com>
#
# This program is free software: you can Use, Study, Modify and Redistribute
# it under the terms of the GNU General Public License version 3, or (at your
# option) any later version, as published by the Free Software Foundation.
#
# You can also Link and Combine this program with other software covered by
# the terms of any of the Free Software licenses or any of the Open Source
# Initiative approved licenses and Convey the resulting work. Corresponding
# source of such a combination shall include the source code for all other
# software used.
#
# This program is distributed WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See COPYING file for full licensing terms.
# See https://www.nexedi.com/licensing for rationale and options.
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

allow_type(np.timedelta64)
allow_type(type(np.c_))

import sklearn.linear_model
allow_class(sklearn.linear_model.LinearRegression)

# allow write access to ndarray, DataFrame, ZBigArray and RAMArray objects
from Products.ERP5Type.patches.Restricted import allow_full_write  # TODO(zope4py2): we need a better place to import this (why not in RestrictedPython ?)
allow_full_write(np.ndarray)
allow_full_write(np.core.records.recarray)
allow_full_write(np.core.records.record)

from wendelin.bigarray.array_zodb import ZBigArray
allow_full_write(ZBigArray)
allow_type(ZBigArray)
from wendelin.bigarray.array_ram import RAMArray
allow_full_write(RAMArray)
allow_type(RAMArray)
