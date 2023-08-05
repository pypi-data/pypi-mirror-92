from injecta.container.ContainerInterface import ContainerInterface

class AbstractDecorator:

    _function: callable = None

    @property
    def function(self):
        return self._function

    def onExecution(self, container: ContainerInterface):
        pass

    def __call__(self, *args, **kwargs):
        pass
