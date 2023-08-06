import sys, os
import argparse
import json

from hpogrid.components.defaults import *
from hpogrid.configuration import ConfigurationBase

                               
class GridConfiguration(ConfigurationBase):
    
    config_type = 'grid'
    description = 'Manage configuration for grid job submission'
    usage = 'hpogrid grid_config <action> <config_name> [<options>]'
    list_columns = ['Grid Configuration']
    show_columns = ['Attribute', 'Value']  
    json_interpreted = []
    
    @staticmethod
    def get_parser_test():
        parser, subparsers = ConfigurationBase.get_parser_test(
            description='Manage configuration for grid job submission',
            usage='hpogrid grid_config <action> <config_name> [<options>')
        for action in subparsers.choices:
            subparsers.choices[action].usage = subparsers.choices[action].usage.replace('<config_type>', 'grid_config')
        for action in ['create', 'update', 'recreate']:
            parser_action = subparsers.choices.get(action, None)
            if parser_action is None:
                raise RuntimeError('Subparser {} not found'.format(action))
            parser_action.add_argument('name', help = "Name given to the configuration file")
            parser_action.add_argument('-s', '--site', nargs='+',
                                help='Name of the grid site(s) to where the jobs are submitted',
                                default=None)
            parser_action.add_argument('-c', '--container', metavar='',
                                help='Name of the docker or singularity container in which the jobs are run', 
                                required=False, default=kDefaultContainer)
            parser_action.add_argument('-i', '--inDS', metavar='',
                                help='Name of input dataset')
            parser_action.add_argument('-o', '--outDS', metavar='',
                                help='Name of output dataset', 
                                default=kDefaultOutDS)       
            parser_action.add_argument('-r', '--retry',
                                help='Check to enable retrying faild jobs',
                                action='store_true')
        return parser

    def get_parser(self, action=None):
        parser = self.get_base_parser()
        if action in kConfigAction:         
            parser.add_argument('name', help = "Name given to the configuration file")
            parser.add_argument('-s', '--site', nargs='+',
                                help='Name of the grid site(s) to where the jobs are submitted',
                                default=None)
            parser.add_argument('-c', '--container', metavar='',
                                help='Name of the docker or singularity container in which the jobs are run', 
                                required=False, default=kDefaultContainer)
            parser.add_argument('-i', '--inDS', metavar='',
                                help='Name of input dataset')
            parser.add_argument('-o', '--outDS', metavar='',
                                help='Name of output dataset', 
                                default=kDefaultOutDS)       
            parser.add_argument('-r', '--retry',
                                help='Check to enable retrying faild jobs',
                                action='store_true')       
        else:
            parser = super().get_parser(action)
        return parser
