import os
import sys
import json
import fnmatch
import argparse

from hpogrid.utils import stylus

kDefultGridSiteType = ['analysis', 'unified']
kDefaultGridSiteInfo = ['state', 'status', 'maxinputsize', 'maxmemory', 'maxtime']

class GridSiteInfo():
    
    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(description='Show grid site information',
                                         usage='hpogrid sites [<args>]',
                    formatter_class=argparse.RawDescriptionHelpFormatter)          
        parser.add_argument('-n', '--name', metavar='',help='filter grid site names')
        parser.add_argument('-g', '--non_gpu', action='store_true',
            help='show also non gpu sites')
        parser.add_argument('-a', '--non_active', action='store_true',
            help='show also non active sites')
        parser.add_argument('-t', '--site_type', metavar='',nargs='+',
            help='filter sites by type', default=kDefultGridSiteType)
        parser.add_argument('-i', '--info', metavar='',nargs='+',
            help='into to show', default=kDefaultGridSiteInfo)
        return parser
    
    @staticmethod
    def run_parser(args=None):
        parser = GridSiteInfo.get_parser()
        if args is None:
            args = sys.argv[2:]
        kwargs = vars(parser.parse_args(args))
        kwargs['gpu'] = not kwargs.pop('non_gpu', 'False')
        kwargs['active'] = not kwargs.pop('non_active', 'False')
        GridSiteInfo.show(**kwargs)

    @staticmethod
    def show(name=None, gpu=True, active=True, site_type=kDefultGridSiteType,
        info=kDefaultGridSiteInfo):

        grid_site_info = GridSiteInfo.extract(name, gpu, active, site_type, info)
        print(stylus.create_table(grid_site_info, transpose=True))

    @staticmethod
    def list_sites(name=None, gpu=True, active=True, site_type=kDefultGridSiteType):
        grid_site_info = GridSiteInfo.extract(name, gpu, active, site_type)
        return list(grid_site_info.keys())

    @staticmethod
    def extract(name=None, gpu=True, active=True, site_type=kDefultGridSiteType,
        info=kDefaultGridSiteInfo):
        '''
        retrieve some basic information of PanDA grid sites
        '''
        try:
            jsonfileLocation = os.environ['ALRB_cvmfs_repo'] + '/sw/local/etc/agis_schedconf.json'
        except:
            jsonfileLocation = '/cvmfs/atlas.cern.ch/repo/sw/local/etc/agis_schedconf.json'
        
        if not os.path.exists(jsonfileLocation):
            raise ValueError('cannot locate file containing grid site information: agis_schedconf.json')
            
        with open(jsonfileLocation,'r') as jsonfile:
            jsondata = json.load(jsonfile)

        if name is None:
            name = '*'

        grid_site_info = {}

        for site in jsondata:
            # filter site names (could also match jsondata[site]['panda_resource'] instead)
            if not fnmatch.fnmatch(site, name):
                continue
            # filter non-active grid sites
            if active and (not jsondata[site]['state'] == 'ACTIVE'):
                continue
            # no good indicator of a GPU site yet will just judge on site name
            if gpu and (not 'GPU' in jsondata[site]['panda_resource']):
                continue
            if jsondata[site]['type'] not in site_type:
                continue
            grid_site_info[site] = {key: jsondata[site][key] for key in info}

        return grid_site_info