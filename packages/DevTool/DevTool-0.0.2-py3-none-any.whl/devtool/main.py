'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2021-01-12 08:32:28
LastEditors: xiaoshuyui
LastEditTime: 2021-01-12 08:45:31
'''
import sys

sys.path.append('..')
from devtool import BaseParser, __appname__


class Parser(BaseParser):
    def __init__(self, args, appname):
        super().__init__(args, appname)
        self.args = args
        self.parser = super().get_parser()
        self.appname = appname

    def get_parser(self):

        self.parser.add_argument('-v',
                                 '--version',
                                 help='show current version',
                                 action='store_true')

        if len(self.args) > 0:
            for i in self.args:
                self.add_parser(i)

        return self.parser

    def add_parser(self, arg):
        if type(arg) is tuple:
            self.parser.add_argument(arg[0],
                                     arg[1],
                                     help=arg[2],
                                     action='store_true')
        elif type(arg) is dict:
            # pass
            self.parser.add_argument(
                arg['shortName'],
                arg['fullName'],
                type=arg['type'],
                help=arg['help'],
            )
        else:
            raise TypeError('input argument type error')


def script():
    p = Parser([], __appname__)
    parser = p.get_parser()
    args = vars(parser.parse_args())
    
    if args['version']:
        from devtool import __version__
        print(__version__)
        del __version__
        return

if __name__ == "__main__":
    script()
