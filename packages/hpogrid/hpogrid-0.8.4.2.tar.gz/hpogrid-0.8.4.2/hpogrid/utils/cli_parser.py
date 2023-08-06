import sys
import argparse

class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action(self, action):
        if type(action) == argparse._SubParsersAction:
            # inject new class variable for subcommand formatting
            subactions = action._get_subactions()
            if subactions:
                invocations = [self._format_action_invocation(a) for a in subactions]
                self._subcommand_max_length = max(len(i) for i in invocations)

        if type(action) == argparse._SubParsersAction._ChoicesPseudoAction:
            # format subcommand help line
            subcommand = self._format_action_invocation(action) # type: str
            width = self._subcommand_max_length
            help_text = ""
            if action.help:
                help_text = self._expand_help(action)
            return "  {:{width}}     {}\n".format(subcommand, help_text, width=width)

        elif type(action) == argparse._SubParsersAction:
            # process subcommand help section
            msg = '\n'
            for subaction in action._get_subactions():
                msg += self._format_action(subaction)
            return msg
        else:
            return super(CustomHelpFormatter, self)._format_action(action)

        
class CLIParser(argparse.ArgumentParser):
    
    def __init__(self, description='', usage=None, version=''):
        
        # create default usage string
        if usage is None:
            if version:
                usage = "%(prog)s [-v|--version] [-h|--help] <command> [<args>]"
            else:
                usage = "%(prog)s [-h|--help] <command> [<args>]"
    
        super().__init__(description=description,
                         formatter_class=CustomHelpFormatter,
                         usage=usage,
                         add_help=False)
        
        if version: 
            version_str = '%(prog)s version {}'.format(version)
            self.add_argument('-v', '--version',
                              action='version',
                              version=version_str,
                              help="show program's version number")
            
        self.add_argument('-h', '--help', 
                          action="store_true",
                          help='show help') 
        
        self._positionals.title = "The most commonly used commands are"
        
    def set_title(self, title):
        self._positionals.title = title
        
    def error(self, message):
        '''
            Override default behavior on error to print help message instead
        '''
        sys.stderr.write('ERROR: %s\n' % message)
        self.print_help()
        sys.exit(0)
        
    def parse_args(self, args=None, namespace=None, **kwargs):
        # print help if no commands or arguments are given
        if (args is None and len(sys.argv) < 2) or (isinstance(args, list) and len(args) == 0):
            self.print_help()
            sys.exit(0)        
        args = super().parse_args(args=args, namespace=namespace, **kwargs)
        
        # print help if -h or --help are given
        if args.help:
            self.print_help()
            sys.exit(0)
        return args
