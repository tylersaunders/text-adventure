import logging
import yaml
from server.engine.scenario import Scenario
from server.engine.location import Location
from server.engine.object import AdventureObject, Activateable


def load_scenario(path: str) -> Scenario:
    """Accepts a scenario in yaml format and parses it into the objects."""
    with open(path, 'r') as stream:
        try:
            loaded_yaml = yaml.safe_load(stream)
        except yaml.YAMLError:
            logging.exception('Failed to safe_load yaml')

        scenario_yaml = loaded_yaml['scenario']
        scenario = Scenario(scenario_yaml['title'],
                            scenario_yaml['starting_location_id'])

        for loc in scenario_yaml['locations']:
            loc_dict = loc['location']
            location = Location(loc_dict['id'], loc_dict['description'])
            scenario.add_location(location)
            for exit, location_id in loc_dict['exits'].items():
                location.exits[exit] = location_id
            if 'objects' in loc_dict:
                for item in loc_dict['objects']:
                    location.objects.append(item)
            logging.debug(location)

        for item in scenario_yaml['items']:
            item_dict = item['item']
            if item_dict['base_object'] == 'activatable':
                obj = Activateable(
                    item_dict['id'],
                    item_dict['name'],
                    item_dict['description'],
                    item_dict['on_description'],
                    item_dict['off_description'],
                )
            logging.debug(obj)
            scenario.add_object(obj)

        stream.close()
        return scenario
