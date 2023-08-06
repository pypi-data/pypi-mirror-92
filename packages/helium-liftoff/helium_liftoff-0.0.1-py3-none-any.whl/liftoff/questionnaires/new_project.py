from liftoff.core.enums import ProjectType, DatabaseType
from liftoff.core.vars import PROJECT_PATH
from liftoff.core.prompt import LiftoffPrompt
from os.path import basename
from .base import Questionnaire


class NewProjectQuestionnaire(Questionnaire):
    @staticmethod
    def prompt():
        config = {}

        # config['project_type'] = LiftoffPrompt(text='projects Type',
        #                                        options=[t.value for t in ProjectType],
        #                                        default=1).prompt()

        # config['project_name'] = LiftoffPrompt(text='projects Name',
        #                                        default=basename(PROJECT_PATH)).prompt()

        config['hostname'] = LiftoffPrompt(text='Local Domain Name (e.g. my-app.local, local.my-app.com)').prompt()

        # config['db_type'] = LiftoffPrompt(text='Local Database Type',
        #                                   options=[t.value for t in DatabaseType],
        #                                   default=1).prompt()
        #
        # if config['db_type'] != DatabaseType.NONE.value:
        #     config['db_name'] = LiftoffPrompt(text='Local Database Name',
        #                                       default=config['project_name']).prompt()
        #
        #     config['db_username'] = LiftoffPrompt(text='Local Database Username',
        #                                           default=config['project_name']).prompt()
        #
        #     config['db_password'] = LiftoffPrompt(text='Local Database Password',
        #                                           default=config['project_name']).prompt()

        return config
