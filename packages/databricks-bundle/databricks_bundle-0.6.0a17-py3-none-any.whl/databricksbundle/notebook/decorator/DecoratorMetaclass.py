# pylint: disable = protected-access
from types import FunctionType
from databricksbundle.notebook.decorator.ContainerManager import ContainerManager

class DecoratorMetaclass(type):

    def __new__(cls, name, bases, attrs):
        originalInit = attrs['__init__']
        initedFunctions = list()

        def decorateCall(decorator, fun):
            initedFunctions.append(fun.__name__)

            if cls._notebookFunctionExecuted(fun):
                decorator._function = fun
                decorator._result = decorator.onExecution(ContainerManager.getContainer())
                return decorator

            return fun

        def decorateInit(decorator, *args, **kwargs):
            if args and isinstance(args[0], FunctionType) and args[0].__name__ not in initedFunctions:
                decoratorName = decorator.__class__.__name__
                raise Exception(f'Use @{decoratorName}() instead of @{decoratorName} please')

            originalInit(decorator, *args, **kwargs)

        attrs['__init__'] = decorateInit
        attrs['__call__'] = decorateCall

        return super().__new__(cls, name, bases, attrs)

    @staticmethod
    def _notebookFunctionExecuted(fun):
        return fun.__module__ == '__main__'
