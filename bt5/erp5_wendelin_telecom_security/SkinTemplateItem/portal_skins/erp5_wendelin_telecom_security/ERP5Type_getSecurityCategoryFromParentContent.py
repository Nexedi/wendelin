"""
This script returns a list of dictionaries which represent
the security groups which a person is member of. It extracts
the categories from the specified items related to the current content.

The parameters are

  base_category_list -- list of category values we need to retrieve
  user_name          -- string obtained from getSecurityManager().getUser().getId()
  ob                 -- object which we want to assign roles to
  portal_type        -- portal type of object
"""


if object is None:
  return []

object = object.getParentValue()

if object is None:
  return []

return object.ERP5Type_getSecurityCategoryFromContent(base_category_list, user_name, object, portal_type)
