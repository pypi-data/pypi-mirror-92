from cement import Controller, ex
from liftoff.builders.projects.laravel import LaravelBuilder
from liftoff.builders.liftoff import LiftoffBuilder
from liftoff.core.vars import PROJECT_PATH
from os.path import dirname, isfile
import json


class Build(Controller):
    class Meta:
        label = 'build'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(help='Initialize the current project using the saved configuration')
    def build(self):
        LiftoffBuilder.build()
        config = self.find_config()
        LaravelBuilder.build(config)

    def find_config(self):
        path = PROJECT_PATH
        config_path = None

        while path != '/' and config_path is None:
            try_path = f"{path}/.liftoff/config.json"

            if isfile(try_path):
                config_path = try_path

            path = dirname(path)

        if config_path is None:
            print("Could not find liftoff project configuration in the current or any parent directories.")
            exit(0)

        with open(config_path) as file:
            data = json.load(file)

        return data
