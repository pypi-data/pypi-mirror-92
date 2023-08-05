from databricksbundle.notebook.decorator.AbstractDecorator import AbstractDecorator

class ResultDecorator(AbstractDecorator):

    _result = None

    @property
    def result(self):
        return self._result
