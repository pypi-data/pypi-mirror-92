import sys, os
import argparse
import json

from hpogrid.components.defaults import *
from hpogrid.components import validation
from hpogrid.configuration import ConfigurationBase
from json import JSONDecodeError

class SearchSpaceConfiguration(ConfigurationBase):

    config_type = 'search_space'
    description = 'Manage configuration for hyperparameter search space'
    usage = 'hpogrid search_space <action> <config_name> <search_space_definition>'
    list_columns = ['Search Space Configuration']
    show_columns = ['Hyperparameters', 'Search Space']  
    json_interpreted = []
    
    @staticmethod
    def get_parser_test():
        parser, subparsers = ConfigurationBase.get_parser_test(
            description='Manage configuration for hyperparameter search space',
            usage='hpogrid search_space <action> <config_name> <search_space_definition>')
        for action in subparsers.choices:
            subparsers.choices[action].usage = subparsers.choices[action].usage.replace('<config_type>', 'search_space')
        for action in ['create', 'update', 'recreate']:
            parser_action = subparsers.choices.get(action, None)
            if parser_action is None:
                raise RuntimeError('Subparser {} not found'.format(action))
            parser_action.add_argument('name', metavar='',
                help='Name given to the search space file')  
            parser_action.add_argument('search_space',metavar='', 
                help='A json decodable string defining the search space')  
        return parser

    def get_parser(self, action=None):
        parser = self.get_base_parser()               
        if action in kConfigAction:     
            parser.add_argument('name', 
                help='Name given to the configuration file')  
            parser.add_argument('search_space', 
                help='A json decodable string defining the search space')  
        else:
            parser = super().get_parser(action)
        return parser

    def configure(self, args, action='create'):

        config = vars(args)
        config_name = config.pop('name', None)
        search_space = config.pop('search_space', None)

        try:
            search_space = json.loads(search_space)
        except JSONDecodeError:
            print('ERROR: Cannot to decode input string into json format. Please check your input.')
            return None

        if action == 'update':
            config_path = self.get_config_path(config_name)
            if not os.path.exists(config_path):
                raise FileNotFoundError('Search space file {} not found. Update aborted.'.format(config_path))
            old_serach_space = json.load(open(config_path))
            search_space = {**old_serach_space, **search_space}
        
        if validation.validate_search_space(search_space):
            self.save(search_space, config_name, action)
        return search_space