from cement import Controller, ex
from liftoff.core.docker_compose import restart_liftoff


class Restart(Controller):
    class Meta:
        label = 'restart'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(help='Restart Liftoff')
    def restart(self):
        restart_liftoff()
