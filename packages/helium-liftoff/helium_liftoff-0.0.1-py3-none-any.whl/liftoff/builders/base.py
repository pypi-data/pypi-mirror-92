from abc import ABC, abstractmethod
from liftoff.app import app


class Builder(ABC):
    @staticmethod
    @abstractmethod
    def build(config):
        pass

    @staticmethod
    def render_template_to_file(data: dict, template: str, path: str):
        content = app().render(data, template, None)

        with open(path, 'w') as file:
            file.write(content)
