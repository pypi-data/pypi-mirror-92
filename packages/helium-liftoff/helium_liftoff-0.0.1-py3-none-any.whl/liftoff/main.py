from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import LiftoffError
from .controllers.base import Base
from .controllers.init import Init
from .controllers.start import Start
from .controllers.stop import Stop
from .controllers.restart import Restart
from .controllers.build import Build
from os import system
from liftoff.app import app

# configuration defaults
CONFIG = init_defaults('liftoff')
CONFIG['liftoff']['foo'] = 'bar'


class Liftoff(App):
    """Liftoff primary application."""

    class Meta:
        label = 'liftoff'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
            Init,
            Build,
            Start,
            Stop,
            Restart
        ]


class LiftoffTest(TestApp,Liftoff):
    """A sub-class of Liftoff that is better suited for testing."""

    class Meta:
        label = 'liftoff'


def main():
    with app(Liftoff()) as a:
        try:
            system('sudo -k')
            a.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            a.exit_code = 1

            if a.debug is True:
                import traceback
                traceback.print_exc()

        except LiftoffError as e:
            print('LiftoffError > %s' % e.args[0])
            a.exit_code = 1

            if a.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            a.exit_code = 0


if __name__ == '__main__':
    main()
