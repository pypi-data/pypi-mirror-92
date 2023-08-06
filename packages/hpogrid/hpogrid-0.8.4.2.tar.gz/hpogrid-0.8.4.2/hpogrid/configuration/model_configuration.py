import sys, os
import argparse
import json

from hpogrid.components.defaults import *
from hpogrid.configuration import ConfigurationBase

class ModelConfiguration(ConfigurationBase):

    config_type = 'model'
    description = 'Manage configuration for machine learning model'
    usage = 'hpogrid model_config <action> <config_name> [<options>]'
    list_columns = ['Model Configuration']
    show_columns = ['Attribute', 'Value']  
    json_interpreted = ['param']
    
    @staticmethod
    def get_parser_test():
        parser, subparsers = ConfigurationBase.get_parser_test(
            description='Manage configuration for the machine learning model',
            usage='hpogrid model_config <action> <config_name> [<options>')
        for action in subparsers.choices:
            subparsers.choices[action].usage = subparsers.choices[action].usage.replace('<config_type>', 'model_config')
        for action in ['create', 'update', 'recreate']:
            parser_action = subparsers.choices.get(action, None)
            if parser_action is None:
                raise RuntimeError('Subparser {} not found'.format(action))
            parser_action.add_argument('name', help= "Name given to the configuration file")            
            parser_action.add_argument('-s','--script', metavar='',
                help='Name of the training script where the function or class that defines'
                     ' the training model will be called to perform the training')
            parser_action.add_argument('-m','--model', metavar='',
                help='Name of the function or class that defines the training model')        
            parser_action.add_argument('-p','--param', metavar='',
                help='Extra parameters to be passed to the training model',
                default=kDefaultModelParam)
        return parser

    def get_parser(self, action=None):
        parser = self.get_base_parser()              
        if action in kConfigAction:  
            parser.add_argument('name', help= "Name given to the configuration file")            
            parser.add_argument('-s','--script', metavar='',
                help='Name of the training script where the function or class that defines'
                     ' the training model will be called to perform the training')
            parser.add_argument('-m','--model', metavar='',
                help='Name of the function or class that defines the training model')        
            parser.add_argument('-p','--param', metavar='',
                help='Extra parameters to be passed to the training model',
                default=kDefaultModelParam)
        else:
            parser = super().get_parser(action)
        return parser
