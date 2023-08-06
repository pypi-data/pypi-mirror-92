from abc import ABC, abstractmethod
from stringcase import snakecase


class Questionnaire(ABC):
    @staticmethod
    @abstractmethod
    def prompt():
        pass

    @staticmethod
    def _to_snake(original: str, title: str):
        snake = snakecase(original)

        if snake != original:
            print(f'Converting {title} "{original}" to "{snake}"')
            print()

        return snake
