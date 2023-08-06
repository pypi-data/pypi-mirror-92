from liftoff.questionnaires.base import Questionnaire
from liftoff.questionnaires.projects.php import PhpQuestionnaire


class LaravelQuestionnaire(Questionnaire):
    @staticmethod
    def prompt():
        config = PhpQuestionnaire.prompt()

        return config
