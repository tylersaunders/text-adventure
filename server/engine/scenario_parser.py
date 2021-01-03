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

        scenario_yaml = loaded_yaml.get('scenario')
        title = scenario_yaml.get('title')
        greeting = scenario_yaml.get('greeting')
        starting_location_id = scenario_yaml.get('starting_location_id')
        scenario = Scenario(title, greeting, starting_location_id)

        for loc in scenario_yaml['locations']:
            loc_dict = loc.get('location')
            location = Location(
                loc_dict.get('id'),
                loc_dict.get('description'),
            )
            scenario.add_location(location)
            for exit, location_id in loc_dict.get('exits', []).items():
                location.exits[exit] = location_id
            if 'objects' in loc_dict:
                for item in loc_dict.get('objects'):
                    location.objects.append(item)
            logging.debug(location)

        for item in scenario_yaml.get('items', []):
            item_dict = item.get('item')
            if item_dict.get('base_object', None) == 'activatable':
                obj = Activateable(
                    item_dict.get('id'),
                    item_dict.get('name'),
                    item_dict.get('description'),
                    item_dict.get('on_description'),
                    item_dict.get('off_description'),
                    takeable=bool(item_dict.get('takeable', False)),
                    active=bool(item_dict.get('active', False)),
                )
            else:
                obj = AdventureObject(
                    item_dict.get('id'),
                    item_dict.get('name'),
                    item_dict.get('description'),
                    takeable=bool(item_dict.get('takeable', False)),
                )
            logging.debug(obj)
            scenario.add_object(obj)

        stream.close()
        return scenario
