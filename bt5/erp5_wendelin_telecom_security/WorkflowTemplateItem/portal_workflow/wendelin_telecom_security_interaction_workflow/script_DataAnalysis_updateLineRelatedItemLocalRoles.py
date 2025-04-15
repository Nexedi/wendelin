tag = script.id
activate_kw = dict(tag=tag)

data_analysis = state_change['object']
data_analysis.reindexObject(activate_kw=activate_kw)

data_analysis_lines = data_analysis.contentValues(portal_type='Data Analysis Line')
if len(data_analysis_lines) == 0:
  return

for data_analysis_line in data_analysis_lines:
  data_analysis_line.activate(after_tag=tag).updateLocalRolesOnSecurityGroups()
  for value in data_analysis_line.getAggregateValueList():
    value.activate(after_tag=tag).updateLocalRolesOnSecurityGroups()
    try:
      content_values = value.contentValues()
      for content_value in content_values:
        content_value.activate(after_tag=tag).updateLocalRolesOnSecurityGroups()
    except AttributeError:
      pass
