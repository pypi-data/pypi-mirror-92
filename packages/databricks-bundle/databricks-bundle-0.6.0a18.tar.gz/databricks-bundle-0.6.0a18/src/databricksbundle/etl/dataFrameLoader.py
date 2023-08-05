# pylint: disable = invalid-name, not-callable
from injecta.container.ContainerInterface import ContainerInterface
from databricksbundle.display import display
from databricksbundle.notebook.decorator.DecoratorMetaclass import DecoratorMetaclass
from databricksbundle.notebook.decorator.ResultDecorator import ResultDecorator
from databricksbundle.notebook.function.ArgumentsResolver import ArgumentsResolver
from databricksbundle.notebook.function.functionInspector import inspectFunction

class dataFrameLoader(ResultDecorator, metaclass=DecoratorMetaclass):

    def __init__(self, *args, **kwargs):
        self._decoratorArgs: tuple = args
        self._displayEnabled = kwargs.get('display', False)

    def onExecution(self, container: ContainerInterface):
        argumentsResolver: ArgumentsResolver = container.get(ArgumentsResolver)
        arguments = argumentsResolver.resolve(inspectFunction(self._function), self._decoratorArgs)

        result = self._function(*arguments)

        if self._displayEnabled:
            display(result)

        return result
