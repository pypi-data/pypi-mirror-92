# pylint: disable = invalid-name, not-callable
from injecta.container.ContainerInterface import ContainerInterface
from databricksbundle.display import display as displayFunction
from databricksbundle.notebook.decorator.DecoratorMetaclass import DecoratorMetaclass
from datalakebundle.notebook.decorator.BaseDecorator import BaseDecorator
from datalakebundle.notebook.decorator.DuplicateColumnsChecker import DuplicateColumnsChecker

class transformation(BaseDecorator, metaclass=DecoratorMetaclass):

    def __init__(self, *args, display=False, checkDuplicateColumns=True): # pylint: disable = unused-argument
        self._display = display
        self._checkDuplicateColumns = checkDuplicateColumns

    def afterExecution(self, container: ContainerInterface):
        if self._checkDuplicateColumns:
            duplicateColumnsChecker: DuplicateColumnsChecker = container.get(DuplicateColumnsChecker)

            dataFrameDecorators = tuple(decoratorArg for decoratorArg in self._decoratorArgs if isinstance(decoratorArg, BaseDecorator))
            duplicateColumnsChecker.check(self._result, dataFrameDecorators)

        if self._display:
            displayFunction(self._result)
