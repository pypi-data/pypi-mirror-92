from cement import Controller, ex
from liftoff.core.docker_compose import stop_liftoff


class Stop(Controller):
    class Meta:
        label = 'stop'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(help='Stop Liftoff')
    def stop(self):
        stop_liftoff()
