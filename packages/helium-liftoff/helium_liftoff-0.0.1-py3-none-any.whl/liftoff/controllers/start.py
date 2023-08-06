from cement import Controller, ex
from liftoff.core.docker_compose import start_liftoff


class Start(Controller):
    class Meta:
        label = 'start'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(help='Start Liftoff')
    def start(self):
        start_liftoff()
