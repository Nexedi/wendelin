# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2018 Nexedi SA and Contributors. All Rights Reserved.
#                    Klaus Wölfel <klaus@nexedi.com>
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
import numpy as np
from erp5.component.document.DataArray import DataArray
from Products.ERP5Type.Base import TempBase
from Products.ERP5Type.Utils import createExpressionContext, \
  evaluateExpressionFromString

class GetIndex(TempBase):
  def __getitem__(self, idx):
    return idx

class DataArrayViewLine(DataArray):
  """
  Data Array like view on one or multiple Data Arrays
  """

  def initArray(self, shape, dtype):
    """
    Not Implemented.
    """
    raise NotImplementedError

  def getArray(self, default=None):
    """
    Get numpy view of Parent Data Array according to index.
    """
    getindex = GetIndex("getindex")
    index = evaluateExpressionFromString(
      createExpressionContext(None, portal=getindex),
      "python: portal[%s]" %self.getIndexExpression()
    )
    # if missing predecessor return the default
    predecessor_value = self.getPredecessorValue()
    if predecessor_value is None:
      return default
    zbigarray = predecessor_value.getArray()
    try:
      array_view = zbigarray[index]
    except TypeError:
      array = zbigarray[:]
      new_dtype = np.dtype({name:array.dtype.fields[name] for name in index})
      array_view = np.ndarray(array.shape, new_dtype, array, 0, array.strides)
    name_list = self.getNameList()
    dtype_expression = self.getDtypeExpression()
    if dtype_expression is not None or name_list:
      if dtype_expression is None:
        dtype = np.dtype(array_view.dtype)
      else:
        dtype = evaluateExpressionFromString(
        createExpressionContext(None, portal=getindex),
        dtype_expression)
      dtype.names = name_list
      return array_view.view(dtype=dtype)
    return array_view
