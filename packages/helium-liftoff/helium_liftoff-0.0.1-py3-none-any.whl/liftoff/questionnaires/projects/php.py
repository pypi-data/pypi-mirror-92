from liftoff.core.enums import PhpVersion
from liftoff.core.prompt import LiftoffPrompt
from liftoff.questionnaires.base import Questionnaire


class PhpQuestionnaire(Questionnaire):
    @staticmethod
    def prompt():
        config = {}

        config['php_version'] = LiftoffPrompt(text='PHP Version',
                                              options=[t.value for t in PhpVersion],
                                              default=1).prompt()

        return config
