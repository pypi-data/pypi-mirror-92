from typing import Optional
from box import Box
from datalakebundle.table.config.TableConfig import TableConfig

class TablesConfigManager:

    def __init__(
        self,
        rawTableConfigs: Box,
    ):
        if rawTableConfigs:
            self.__tableConfigs = [TableConfig.fromBox(identifier, rawTableConfig) for identifier, rawTableConfig in rawTableConfigs.items()]
        else:
            self.__tableConfigs = []

    def exists(self, identifier: str) -> bool:
        for tableConfig in self.__tableConfigs:
            if tableConfig.identifier == identifier:
                return True

        return False

    def get(self, identifier: str) -> Optional[TableConfig]:
        for tableConfig in self.__tableConfigs:
            if tableConfig.identifier == identifier:
                return tableConfig

        raise Exception(f'Identifier {identifier} not found among datalakebundle.tables')

    def getByFilter(self, filterFunction: callable):
        return list(filter(filterFunction, self.__tableConfigs))
