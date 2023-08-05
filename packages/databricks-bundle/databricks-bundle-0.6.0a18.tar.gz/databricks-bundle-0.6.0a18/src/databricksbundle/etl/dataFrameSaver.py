# pylint: disable = invalid-name, not-callable
from injecta.container.ContainerInterface import ContainerInterface
from databricksbundle.notebook.decorator.DecoratorMetaclass import DecoratorMetaclass
from databricksbundle.notebook.decorator.AbstractDecorator import AbstractDecorator
from databricksbundle.notebook.function.ArgumentsResolver import ArgumentsResolver
from databricksbundle.notebook.function.functionInspector import inspectFunction

class dataFrameSaver(AbstractDecorator, metaclass=DecoratorMetaclass):

    def __init__(self, *args):
        self._decoratorArgs: tuple = args

    def onExecution(self, container: ContainerInterface):
        argumentsResolver: ArgumentsResolver = container.get(ArgumentsResolver)
        arguments = argumentsResolver.resolve(inspectFunction(self._function), self._decoratorArgs)

        self._function(*arguments)
