# pylint: disable = all
import os
from datalakebundle.notebook.decorator.dataFrameLoader import dataFrameLoader
from datalakebundle.notebook.decorator.transformation import transformation
from datalakebundle.notebook.decorator.dataFrameSaver import dataFrameSaver

os.environ['APP_ENV'] = 'test'

@dataFrameLoader()
def load_data():
    return 155

@dataFrameLoader()
def load_data2():
    return 145

@transformation(load_data, load_data2, checkDuplicateColumns=False)
def sumup(police_number: int, something: int):
    assert police_number == 155
    assert something == 145

    return 155 + 145

@dataFrameSaver(sumup)
def save(result: int):
    assert result == 300

if __name__ == '__main__':
    assert isinstance(load_data, dataFrameLoader)
    assert isinstance(load_data2, dataFrameLoader)
    assert isinstance(sumup, transformation)
    assert isinstance(save, dataFrameSaver)
