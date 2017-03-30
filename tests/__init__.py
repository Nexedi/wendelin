from test_suite import ERP5TypeTestSuite
import glob
import os.path
import re
import sys

HERE = os.path.dirname(__file__)
BT5 = os.path.join(os.path.split(HERE)[0],'bt5')


class WendelinERP5(ERP5TypeTestSuite):


  def getTestList(self):
    component_re = re.compile(".*/([^/]+)/TestTemplateItem/portal_components"
                              "/test\.[^.]+\.([^.]+).py$")
    return ['%s:%s' % (x.group(1), x.group(2)) \
      for x in [component_re.match(y) for y in glob.glob(os.path.join(
      BT5, '*', '*', '*', 'test.erp5.test*.py'))]]
    
    
class ERP5(ERP5TypeTestSuite):
  mysql_db_count = 3

  def _getAllERP5TestList(self):
    test_list = []
    #xxx: this is implemented in a hackish way
    path = os.path.join(os.path.split(sys.path[0])[0], 'erp5')
    component_re = re.compile(".*/([^/]+)/TestTemplateItem/portal_components"
                              "/test\.[^.]+\.([^.]+).py$")

    for test_path in (
      glob.glob('%s/product/*/tests/test*.py' % path) +
      glob.glob('%s/bt5/*/TestTemplateItem/test*.py' % path) +
      glob.glob('%s/bt5/*/TestTemplateItem/portal_components/test.*.test*.py' % path)):
      component_re_match = component_re.match(test_path)
      if component_re_match is not None:
        test_case = "%s:%s" % (component_re_match.group(1),
                               component_re_match.group(2))
      else:
        test_case = test_path.split(os.sep)[-1][:-3]
      product = test_path.split(os.sep)[-3]
      # don't test 3rd party products
      if product in ('PortalTransforms', 'MailTemplates', 'Zelenium'):
        continue
      # ERP5TioSafe is disabled for now because it requires external programs
      # such as php and it has not been updated for Zope >= 2.12
      if product == 'ERP5TioSafe':
        continue
      test_list.append(test_case)
    return test_list

  def run(self, full_test):
    test = ':' in full_test and full_test.split(':')[1] or full_test
    if test in ('testConflictResolution', 'testInvalidationBug'):
      status_dict = self.runUnitTest('--save', full_test)
      if not status_dict['status_code']:
        status_dict = self.runUnitTest('--load', '--activity_node=2', full_test)
      return status_dict
    return super(ERP5, self).run(full_test)


  def getTestList(self): 
    test_list = []

    for full_test_case in self._getAllERP5TestList():
      test_case = (':' in full_test_case and full_test_case.split(':')[1]
                   or full_test_case)

      # skip some tests
      if test_case.startswith('testLive') or test_case.startswith('testVifib') \
         or test_case.find('Performance') > 0 \
         or test_case in ('testERP5LdapCatalog', # XXX (Ivan), until LDAP server is available this test will alway fail
                          # tests reading selenium tables from erp5.com
                          # not maintained
                          'testFunctionalConfigurator',
                          'testFunctionalConfiguratorConsulting',
                          'testERP5eGov',
                          'testAccounting_l10n_fr_m9',
                          # Not a test
                          'testERP5SyncMLMixin'
         ):
        continue
      test_list.append(full_test_case)
    return test_list
