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

import numpy as np

allow_type(np.dtype)

sz = np.array([('2017-07-12T12:30:20',)], dtype=[('date', 'M8[s]')])
allow_type(type(sz[0]['date']))

allow_module('sklearn')
allow_module('sklearn.model_selection')
allow_module('sklearn.linear_model')
allow_module('scipy')

allow_module('wendelin.bigarray.array_zodb')

import sklearn.linear_model
allow_class(sklearn.linear_model.LinearRegression)

# allow write access to ndarray, DataFrame, ZBigArray and RAMArray objects
def allow_full_write(t):
  """Allow setting and deleting items and attributes for this type.

  This supports both RestrictedPython-3.6.0, where the safetype is implemented as:

      safetype = {dict: True, list: True}.has_key
      ...
      safetype(t)

  and RestrictedPython-5.1, where the safetype is implemented as:

      safetypes = {dict, list}
      ...
      safetype(t)

  """
  from RestrictedPython.Guards import full_write_guard
  safetype = full_write_guard.__closure__[1].cell_contents
  if isinstance(safetype, set): # 5.1
    safetype.add(t)
  else: # 3.6
    safetype.__self__.update({t: True})


allow_full_write(np.ndarray)
allow_full_write(np.core.records.recarray)
allow_full_write(np.core.records.record)

from wendelin.bigarray.array_zodb import ZBigArray
allow_full_write(ZBigArray)
allow_type(ZBigArray)
from wendelin.bigarray.array_ram import RAMArray
allow_full_write(RAMArray)
allow_type(RAMArray)
