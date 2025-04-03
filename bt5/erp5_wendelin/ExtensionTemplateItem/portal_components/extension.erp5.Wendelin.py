# -*- coding: utf-8 -*-
"""
 Wendelin extensions code.
"""
from wendelin.bigarray.array_zodb import ZBigArray
import numpy as np
from ZODB.utils import u64
try:  # duplication wrt neo/client/patch
  from ZODB.Connection import TransactionMetaData
except ImportError: # BBB: ZODB < 5
  from ZODB.BaseStorage import TransactionRecord
  TransactionMetaData = lambda user='', description='', extension=None: \
      TransactionRecord(None, None, user, description, extension)


def DataStream_copyCSVToDataArray(data_stream, chunk_list, start, end, \
                                  data_array_reference=None):
  """
    Receive CSV data and transform it to a numpy array of floats.
  """
  chunk_text = ''.join(chunk_list)

  # compensate possible offset mistmatch
  last_new_line_index = chunk_text.rfind('\n')
  offset_mismatch = len(chunk_text) - last_new_line_index -1
  start = start - offset_mismatch
  end = end - offset_mismatch
  
  #data_stream.log(chunk_text)

  # remove offset line which is to be processed next call
  chunk_text = chunk_text[:len(chunk_text) - offset_mismatch - 1]
  
  # process left data
  line_list = chunk_text.split('\n')
  size_list = []
  for line in line_list:
    line_item_list = line.split(',')
    size_list.extend([x for x in line_item_list])

  # save this value as a numpy array (for testing, only create ZBigArray for one variable)
  #data_stream.log(size_list)
  size_list = [float(x) for x in size_list]
  ndarray = np.array(size_list)

  data_array = data_stream.portal_catalog.getResultValue( \
                      portal_type='Data Array', \
                      reference = data_array_reference, \
                      validation_state = 'validated')
  zarray = data_array.getArray()
  if zarray is None:
    # first time init
    zarray = ZBigArray((0,), ndarray.dtype)
    data_array.setArray(zarray)
    zarray = data_array.getArray()

  #data_stream.log('Zarray shape=%s,  To append shape=%s, %s' %(zarray.shape, ndarray.shape, ndarray.itemsize))
    
  # resize so we can add new array data
  old_shape = zarray.shape
  ndarray_shape = ndarray.shape
  new_one = old_shape[0] + ndarray_shape[0]
  zarray.resize((new_one,))
    
  # add new array data to persistent ZBigArray
  zarray[-ndarray_shape[0]:] = ndarray
  
  return start, end


def Base_deleteZBigArray(zbigarray):
  """'Base_deleteZBigArray' explicitly garbage collects zbigarray.
  In order to free storage space, the DB needs to be packed after GC.
  """
  conn = zbigarray._p_jar
  storage = conn.db().storage

  def rm(obj):
    obj._p_activate()
    storage.deleteObject(obj._p_oid, obj._p_serial, txn)
    obj._p_deactivate()

  txn = TransactionMetaData(description='Base_deleteZBigArray(0x%x)' % u64(zbigarray._p_oid))
  try:
    storage.tpc_begin(txn)
    zfile = zbigarray.zfile
    blktab = zfile.blktab
    for b in blktab.values():
      rm(b)
    for obj in (blktab, zfile, zbigarray):
      rm(obj)
    storage.tpc_vote(txn)
    storage.tpc_finish(txn)
  except:
    storage.tpc_abort(txn)
    raise

