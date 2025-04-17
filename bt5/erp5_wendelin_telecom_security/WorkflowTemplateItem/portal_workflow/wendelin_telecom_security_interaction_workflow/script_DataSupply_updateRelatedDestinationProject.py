data_supply = state_change['object']

destination_project = data_supply.getDestinationProject()
for value in data_supply.Base_getRelatedObjectList():
  if value.getSimulationState() == 'started':
    value.setDestinationProject(destination_project)
