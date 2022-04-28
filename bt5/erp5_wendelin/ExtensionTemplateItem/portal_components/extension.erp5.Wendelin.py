# -*- coding: utf-8 -*-
"""
 Wendelin extensions code.
"""
import os
import urllib2
import urlparse

from wendelin.bigarray.array_zodb import ZBigArray
import numpy as np
import pandas as pd
from zExceptions import Unauthorized


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


# https://github.com/pandas-dev/pandas/blob/12b3264d17780b6b38f747353bc80cfd910e6dc8/pandas/io/common.py#L64
_VALID_URLS = set(
  urlparse.uses_relative +
  urlparse.uses_netloc +
  urlparse.uses_params
)
_VALID_URLS.discard('')


# This is how pandas checks if a string is an url
# https://github.com/pandas-dev/pandas/blob/12b3264d17780b6b38f747353bc80cfd910e6dc8/pandas/io/common.py#L116
def _is_url(url):
  try:
    return urlparse.urlparse(url).scheme in _VALID_URLS
  except urllib2.URLError:
    return False

# This is how pandas checks if the given string is a file path
# See https://github.com/pandas-dev/pandas/blob/0.19.x/pandas/io/json.py#L253
def _does_file_exist(file_path):
  try:
    return os.path.exists(file_path)
  # If the filepath is too long will raise here
  except (TypeError, ValueError):
    return False


def Base_readJson(json_string, *args, **kwargs):
  """
    Parse json to pandas DataFrame.
  
  This function is a wrapper of pandas "read_json"
  which limits the functionality of the wrapped function:
  only json strings are allowed as inputs, files
  or file paths or urls are prohibited (due to security
  concerns).

  Please consult the pandas documentation for arguments
  and keyword-arguments:

  https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_json.html#pandas-read-json
  """

  # File like objects are prohibited
  if not isinstance(json_string, str) or hasattr(json_string, 'read'):
    raise Unauthorized("Can only parse str.")

  # Prohibit any string which pandas could understand as an url or
  # as a file path.
  if _is_url(json_string) or _does_file_exist(json_string):
    raise Unauthorized("Can't parse file names or urls.")
  
  # If the given argument is neither a file path nor
  # a file, then it must be a json string (or gibberish).
  # We can safely pass it to pandas.
  return pd.read_json(json_string, *args, **kwargs)