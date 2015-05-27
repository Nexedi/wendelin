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

