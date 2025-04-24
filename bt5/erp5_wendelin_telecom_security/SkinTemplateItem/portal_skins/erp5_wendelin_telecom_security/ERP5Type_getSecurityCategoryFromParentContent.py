"""
This script returns a list of dictionaries which represent
the security groups which a person is member of. It extracts
the categories from the specified items related to the current content.

The parameters are

  base_category_list -- list of category values we need to retrieve
  user_name          -- string obtained from getSecurityManager().getUser().getId()
  obj                -- object which we want to assign roles to
  portal_type        -- portal type of object
"""


if obj is None:
  return []

parent_obj = obj.getParentValue()

if parent_obj is None:
  return []

return parent_obj.ERP5Type_getSecurityCategoryFromContent(
  base_category_list,
  user_name,
  parent_obj,
  parent_obj.getPortalType()
)
