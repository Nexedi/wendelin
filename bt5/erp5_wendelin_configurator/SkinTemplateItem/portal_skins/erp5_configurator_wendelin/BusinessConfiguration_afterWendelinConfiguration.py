""" 
This script will be called to apply the customization. 
"""

# Activate the knowledge pads on portal home to enable later the Wendelin 
# Information gadget.
#
configuration = context.restrictedTraverse('portal_preferences/default_site_preference')
configuration.setPreferredHtmlStyleAccessTab(True)
