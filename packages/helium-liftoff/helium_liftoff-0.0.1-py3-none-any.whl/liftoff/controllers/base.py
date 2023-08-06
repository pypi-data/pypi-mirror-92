from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version

VERSION_BANNER = """
Liftoff %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'Command line tools for creating local development projects and resources'

        # controller level arguments. ex: 'liftoff --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
        ]


    def _default(self):
        self.app.args.print_help()
