##############################################################################
#
# Copyright (c) 2002-2022 Nexedi SA and Contributors. All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
##############################################################################

from erp5.component.test.WendelinConfiguratorMixin import WendelinConfiguratorMixin

class testWendelinConfiguratorSetupDataSample(WendelinConfiguratorMixin):

  def getConfiguratorOptions(self):
    return {
      "field_your_setup_data_sample": True
    }

  def testConfiguredBusinessTemplateList(self):
    """ Make sure Installed business Templates are
        what it is expected.  """

    expected_business_template_list = self.getCommonBusinessTemplateList()
    expected_business_template_list += ['erp5_wendelin_data_sample']
    self.assertSameSet(expected_business_template_list,
      self.portal.portal_templates.getInstalledBusinessTemplateTitleList())

  def testModuleBusinessApplication(self):
    super(testWendelinConfiguratorSetupDataSample, self).checkModuleBusinessApplication()

  def testSiteTitle(self):
    super(testWendelinConfiguratorSetupDataSample, self).checkSiteTitle()

  def testPreference(self):
    super(testWendelinConfiguratorSetupDataSample, self).checkPreference()
