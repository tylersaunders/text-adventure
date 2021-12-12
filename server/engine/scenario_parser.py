import logging
import yaml
from server.engine.scenario import Scenario
from server.engine.location import Location
from server.engine.object import AdventureObject


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
            location = Location(**loc_dict)
            scenario.add_location(location)
            logging.debug(location)

        for item in scenario_yaml.get('items', []):
            item_dict = item.get('item')
            obj = AdventureObject.parse(**item_dict)
            logging.debug(obj)
            scenario.add_object(obj)

        stream.close()
        return scenario
