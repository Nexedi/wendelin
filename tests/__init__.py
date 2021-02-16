from test_suite import ERP5TypeTestSuite
import glob
import os.path
import re

HERE = os.path.dirname(__file__)
BT5 = os.path.join(os.path.split(HERE)[0],'bt5')


class WendelinERP5(ERP5TypeTestSuite):


  def getTestList(self):
    component_re = re.compile(".*/([^/]+)/TestTemplateItem/portal_components"
                              "/test\.[^.]+\.([^.]+).py$")
    return ['%s:%s' % (x.group(1), x.group(2)) \
      for x in [component_re.match(y) for y in glob.glob(os.path.join(
      BT5, '*', '*', '*', 'test.erp5.test*.py'))]]
  
  def run(self, full_test):
    test = ':' in full_test and full_test.split(':')[1] or full_test
    if test.startswith('testFunctional'):
      return self._updateFunctionalTestResponse(self.runUnitTest(full_test))
    return super(WendelinERP5, self).run(full_test)

  ### this is dublicate code from erp5, needed to display functional tests ontestnodes nicely
  def _updateFunctionalTestResponse(self, status_dict):
    """ Convert the Unit Test output into more accurate information
        related to funcional test run.
    """
    # Parse relevant information to update response information
    try:
      summary, html_test_result = status_dict['stderr'].split("-"*79)[1:3]
    except ValueError:
      # In case of error when parse the file, preserve the original
      # informations. This prevents we have unfinished tests.
      return status_dict
    status_dict['html_test_result'] = html_test_result
    search = self.FTEST_PASS_FAIL_RE.search(summary)
    if search:
      group_dict = search.groupdict()
      status_dict['failure_count'] = int(group_dict['failures'])
      status_dict['test_count'] = int(group_dict['total'])
      status_dict['skip_count'] = int(group_dict['expected_failure'])
    return status_dict
