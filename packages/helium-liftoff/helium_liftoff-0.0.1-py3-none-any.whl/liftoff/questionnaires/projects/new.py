from liftoff.core.enums import ProjectType, DatabaseType
from liftoff.core.vars import PROJECT_PATH
from liftoff.core.prompt import LiftoffPrompt
from liftoff.questionnaires.base import Questionnaire
from os.path import basename
from .laravel import LaravelQuestionnaire


class NewProjectQuestionnaire(Questionnaire):
    @staticmethod
    def prompt():
        config = {}

        config['project_type'] = LiftoffPrompt(text='Project Type',
                                               options=[t.value for t in ProjectType],
                                               default=1).prompt()

        config['project_name'] = LiftoffPrompt(text='Project Name',
                                               default=basename(PROJECT_PATH)).prompt()

        config['hostname'] = LiftoffPrompt(text='Local Domain Name (e.g. local.my-app.com)').prompt()

        config['db_type'] = LiftoffPrompt(text='Local Database Type',
                                          options=[t.value for t in DatabaseType],
                                          default=1).prompt()

        if config['db_type'] != DatabaseType.NONE.value:
            db_name = LiftoffPrompt(text='Local Database Name',
                                    default=config['project_name']).prompt()
            config['db_name'] = Questionnaire._to_snake(db_name, 'Local Database Name')

            db_username = LiftoffPrompt(text='Local Database Username',
                                        default=config['project_name']).prompt()
            config['db_username'] = Questionnaire._to_snake(db_username, 'Local Database Username')

            db_password = LiftoffPrompt(text='Local Database Password',
                                        default=config['project_name']).prompt()
            config['db_password'] = Questionnaire._to_snake(db_password, 'Local Database Password')

        project_config = NewProjectQuestionnaire.__prompt_project(config['project_type'])

        config.update(project_config)

        return config

    @staticmethod
    def __prompt_project(project_type: str):
        if project_type == ProjectType.LARAVEL.value:
            return LaravelQuestionnaire.prompt()
        else:
            return {}
