# -*- coding: utf-8 -*-

import os
from test_suite import ERP5TypeTestSuite
from glob import glob
import os.path
import re
from itertools import chain

HERE = os.path.dirname(__file__)
BT5 = os.path.join(os.path.split(HERE)[0], 'bt5')
PRODUCT = os.path.join(os.path.split(HERE)[0], 'product')

class WendelinERP5(ERP5TypeTestSuite):

  def getTestList(self):
    component_re = re.compile(".*/([^/]+)/TestTemplateItem/portal_components"
                              "/test\.[^.]+\.([^.]+).py$")
    # Separate Wendelin Telecom tests from standard Wendelin tests
    # as they need the dedicated software release to run properly
    return ['%s:%s' % (x.group(1), x.group(2)) \
      for x in [component_re.match(y) for y in glob(os.path.join(
      BT5, '*', '*', '*', 'test.erp5.test*.py'))] \
      if "WendelinTelecom" not in x.group(2)]

  def run(self, full_test):
    test = ':' in full_test and full_test.split(':')[1] or full_test
    # from https://lab.nexedi.com/nexedi/erp5/commit/530e8b4e:
    # ---- 8< ----
    #   Combining Zope and WCFS working together requires data to be on a real
    #   storage, not on in-RAM MappingStorage inside Zope's Python process.
    #   Force this via --load --save for now.
    #
    #   Also manually indicate via --with_wendelin_core, that this test needs
    #   WCFS server - corresponding to ZODB test storage - to be launched.
    #
    #   In the future we might want to rework custom_zodb.py to always use
    #   FileStorage on tmpfs instead of δ=MappingStorage in DemoStorage(..., δ),
    #   and to always spawn WCFS for all tests, so that this hack becomes
    #   unnecessary.
    # ---- 8< ----
    status_dict = self.runUnitTest('--load', '--save', '--with_wendelin_core', full_test)
    if test.startswith('testFunctional'):
      status_dict = self._updateFunctionalTestResponse(status_dict)
    return status_dict

  ### this is dublicate code from erp5, needed to display functional tests ontestnodes nicely
  def _updateFunctionalTestResponse(self, status_dict):
    """ Convert the Unit Test output into more accurate information
        related to funcional test run.
    """
    # Parse relevant information to update response information
    try:
      summary, html_test_result = status_dict['stderr'].split(b"-"*79)[1:3]
    except ValueError:
      # In case of error when parse the file, preserve the original
      # informations. This prevents we have unfinished tests.
      return status_dict
    status_dict['html_test_result'] = html_test_result
    search = self.FTEST_PASS_FAIL_RE.search(summary.decode())
    if search:
      group_dict = search.groupdict()
      status_dict['failure_count'] = int(group_dict['failures'])
      status_dict['test_count'] = int(group_dict['total'])
      status_dict['skip_count'] = int(group_dict['expected_failure'])
    return status_dict

class WendelinTelecomERP5(WendelinERP5):

  def getTestList(self):
    component_re = re.compile(".*/([^/]+)/TestTemplateItem/portal_components"
                              "/test\.[^.]+\.([^.]+).py$")
    # Separate Wendelin Telecom tests from standard Wendelin tests
    # as they need the dedicated software release to run properly
    return ['%s:%s' % (x.group(1), x.group(2)) \
      for x in [component_re.match(y) for y in glob(os.path.join(
      BT5, '*', '*', '*', 'test.erp5.test*.py'))] \
      if "WendelinTelecom" in x.group(2)]

class WendelinBusinessTemplateCodingStyleTestSuite(WendelinERP5):
  """
  Run coding style test on all business templates.
  """

  def getTestList(self):
    test_list = [
      os.path.basename(path)
      for path in chain(
        glob(HERE + '/../bt5/*'),
        glob(HERE + '/../product/Wendelin/bootstrap/*'))
      # we skip coding style check for business templates having this marker
      # property. Since the property is not exported (on purpose), modified business templates
      # will be candidate for coding style test again.
      if not os.path.exists(path + '/bt/skip_coding_style_test') and os.path.isdir(path)
    ]
    for path in chain(glob(HERE + '/../product/*'), glob(HERE + '/../bt5')):
      if not os.path.exists(path + '/skip_coding_style_test') and os.path.isdir(path):
        test_list.append("Python3Style." + os.path.basename(path))

    return test_list

  def run(self, full_test):
    if full_test.startswith("Python3Style."):
      return self.runUnitTest('Python3StyleTest', TESTED_PRODUCT=full_test[13:])
    return self.runUnitTest('CodingStyleTest', TESTED_BUSINESS_TEMPLATE=full_test)

  def getLogDirectoryPath(self, *args, **kw):
    log_directory = os.path.join(
        self.log_directory,
        args[-1] + '-' + (kw.get('TESTED_BUSINESS_TEMPLATE') or kw['TESTED_PRODUCT']))
    os.mkdir(log_directory)
    return log_directory

  pass
