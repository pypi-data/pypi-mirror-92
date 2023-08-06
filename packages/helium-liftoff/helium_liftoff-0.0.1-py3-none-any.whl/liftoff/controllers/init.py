from cement import Controller, ex
from liftoff.questionnaires.projects.new import NewProjectQuestionnaire
from liftoff.builders.projects.laravel import LaravelBuilder
from liftoff.builders.liftoff import LiftoffBuilder


class Init(Controller):
    class Meta:
        label = 'init'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(help='Initialize a new project')
    def init(self):
        LiftoffBuilder.build()
        config = NewProjectQuestionnaire.prompt()
        LaravelBuilder.build(config)
