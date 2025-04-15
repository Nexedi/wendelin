"""
This script returns a list of dictionaries which represent
the security groups which a person is member of. It extracts
the categories from the specified item related to the current content.

The parameters are

  base_category_list -- list of category values we need to retrieve
  user_name          -- string obtained from getSecurityManager().getUser().getId()
  ob                 -- object which we want to assign roles to
  portal_type        -- portal type of object
"""


result_list = []
temp = []

if object is None:
  return []

for related_item in object.Base_getRelatedObjectList(portal_type='Data Supply Line'):
  temp += object.ERP5Type_getSecurityParentCategoryFromContent([base_category_list[0]], user_name, related_item, portal_type)[0][base_category_list[0]]

if len(temp) > 0:
  result_list = [{base_category_list[0]: temp}]
return result_list
