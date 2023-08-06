# pylint: disable = invalid-name, not-callable
from databricksbundle.notebook.decorator.DecoratorMetaclass import DecoratorMetaclass
from datalakebundle.notebook.decorator.BaseDecorator import BaseDecorator

class dataFrameSaver(BaseDecorator, metaclass=DecoratorMetaclass):

    # empty __init__() to suppress PyCharm's "unexpected arguments" error
    def __init__(self, *args):
        pass
