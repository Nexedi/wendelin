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

class testWendelinConfiguratorSetupDataNotebook(WendelinConfiguratorMixin):

  def getConfiguratorOptions(self):
    return {
      "field_your_setup_data_notebook": True
    }

  def testConfiguredBusinessTemplateList(self):
    """ Make sure Installed business Templates are
        what it is expected.  """

    expected_business_template_list = [
      'erp5_code_mirror',
      'erp5_mysql_innodb_catalog',
      'erp5_odt_style',
      'erp5_pdm',
      'erp5_svg_editor',
      'erp5_jquery_plugin_mbmenu',
      'erp5_dhtml_style',
      'erp5_notebook',
      'erp5_base',
      'erp5_xhtml_style',
      'erp5_ods_style',
      'erp5_wendelin_examples',
      'erp5_knowledge_pad',
      'erp5_jquery_ui',
      'erp5_property_sheets',
      'erp5_web_renderjs_ui',
      'erp5_dms',
      'erp5_jquery',
      'erp5_ingestion_mysql_innodb_catalog',
      'erp5_ingestion',
      'erp5_forge',
      'erp5_jquery_plugin_elastic',
      'erp5_core_proxy_field_legacy',
      'erp5_rss_style',
      'erp5_jquery_sheet_editor',
      'erp5_big_file',
      'erp5_jquery_plugin_colorpicker',
      'erp5_web',
      'erp5_project',
      'erp5_jquery_plugin_sheet',
      'erp5_json_type',
      'erp5_core',
      'erp5_font',
      'erp5_configurator',
      'erp5_hal_json_style',
      'erp5_web_service',
      'erp5_development_wizard',
      'erp5_trade',
      'erp5_data_notebook',
      'erp5_wendelin_category',
      'erp5_wendelin_configurator',
      'erp5_configurator_maxma_demo',
      'erp5_accounting',
      'erp5_wendelin_development',
      'erp5_full_text_mroonga_catalog',
      'erp5_oauth2_resource',
      'erp5_wendelin',
      'erp5_jquery_plugin_jqchart',
      'erp5_stock_cache',
      'erp5_simulation',
      'erp5_crm'
    ]
    self.assertSameSet(expected_business_template_list,
      self.portal.portal_templates.getInstalledBusinessTemplateTitleList())

  def testModuleBusinessApplication(self):
    super(testWendelinConfiguratorSetupDataNotebook, self).checkModuleBusinessApplication()

  def testSiteTitle(self):
    super(testWendelinConfiguratorSetupDataNotebook, self).checkSiteTitle()

  def testPreference(self):
    super(testWendelinConfiguratorSetupDataNotebook, self).checkPreference()

