# pylint: disable = too-many-instance-attributes
import pyspark.sql.types as T
from argparse import Namespace
from logging import Logger
from datalakebundle.table.TableExistenceChecker import TableExistenceChecker
from datalakebundle.table.config.TableConfig import TableConfig
from datalakebundle.table.config.TablesConfigManager import TablesConfigManager
from datalakebundle.table.create.TableCreator import TableCreator
from datalakebundle.table.create.TableRecreator import TableRecreator
from datalakebundle.table.delete.TableDeleter import TableDeleter
from datalakebundle.table.optimize.TablesOptimizerCommand import TablesOptimizerCommand
from datalakebundle.table.schema.SchemaGetter import SchemaGetter

class TableManager:

    def __init__(
        self,
        logger: Logger,
        schemaGetter: SchemaGetter,
        tablesConfigManager: TablesConfigManager,
        tableCreator: TableCreator,
        tableRecreator: TableRecreator,
        tableDeleter: TableDeleter,
        tableExistenceChecker: TableExistenceChecker,
        tablesOptimizerCommand: TablesOptimizerCommand,
    ):
        self.__logger = logger
        self.__schemaGetter = schemaGetter
        self.__tablesConfigManager = tablesConfigManager
        self.__tableCreator = tableCreator
        self.__tableRecreator = tableRecreator
        self.__tableDeleter = tableDeleter
        self.__tableExistenceChecker = tableExistenceChecker
        self.__tablesOptimizerCommand = tablesOptimizerCommand

    def getConfig(self, identifier: str) -> TableConfig:
        return self.__tablesConfigManager.get(identifier)

    def getSchema(self, identifier: str) -> T.StructType:
        tableConfig = self.__tablesConfigManager.get(identifier)

        return self.__schemaGetter.get(tableConfig.schemaPath)

    def create(self, identifier: str):
        tableConfig = self.__tablesConfigManager.get(identifier)

        self.__logger.info(f'Creating table {tableConfig.fullTableName} for {tableConfig.targetPath}')

        self.__tableCreator.createEmptyTable(tableConfig)

        self.__logger.info(f'Table {tableConfig.fullTableName} successfully created')

    def recreate(self, identifier: str):
        tableConfig = self.__tablesConfigManager.get(identifier)

        self.__tableRecreator.recreate(tableConfig)

    def delete(self, identifier: str):
        tableConfig = self.__tablesConfigManager.get(identifier)

        self.__tableDeleter.delete(tableConfig)

        self.__logger.info(f'Table {tableConfig.fullTableName} successfully deleted')

    def exists(self, identifier: str):
        tableConfig = self.__tablesConfigManager.get(identifier)

        return self.__tableExistenceChecker.tableExists(tableConfig.dbName, tableConfig.tableName)

    def optimizeAll(self):
        self.__tablesOptimizerCommand.run(Namespace())
