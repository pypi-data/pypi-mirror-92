from box import Box

class TableConfig:

    def __init__(
        self,
        identifier: str,
        dbName: str,
        tableName: str,
        schemaPath: str,
        targetPath: str,
        partitionBy: list = None,
    ):
        self.__identifier = identifier
        self.__dbName = dbName
        self.__tableName = tableName
        self.__schemaPath = schemaPath
        self.__targetPath = targetPath
        self.__partitionBy = partitionBy or []

    @property
    def identifier(self):
        return self.__identifier

    @property
    def tableIdentifier(self):
        return self.__identifier[self.__identifier.find('.') + 1:]

    @property
    def tableName(self):
        return self.__tableName

    @property
    def schemaPath(self):
        return self.__schemaPath

    @property
    def targetPath(self):
        return self.__targetPath

    @property
    def partitionBy(self):
        return self.__partitionBy

    @property
    def fullTableName(self):
        return self.__dbName + '.' + self.__tableName

    @property
    def dbIdentifier(self):
        return self.__identifier[:self.__identifier.find('.')]

    @property
    def dbName(self):
        return self.__dbName

    @staticmethod
    def fromBox(identifier: str, boxConfig: Box) -> 'TableConfig':
        if 'partitionBy' in boxConfig:
            if isinstance(boxConfig.partitionBy, str):
                partitionBy = [boxConfig.partitionBy]
            else:
                partitionBy = boxConfig.partitionBy
        else:
            partitionBy = []

        return TableConfig(
            identifier=identifier,
            dbName=boxConfig.dbName,
            tableName=boxConfig.tableName,
            schemaPath=boxConfig.schemaPath,
            targetPath=boxConfig.targetPath,
            partitionBy=partitionBy
        )

    def __eq__(self, other: 'TableConfig'):
        return (
            self.identifier == other.identifier
            and self.__dbName == other.dbName
            and self.__tableName == other.tableName
            and self.__schemaPath == other.schemaPath
            and self.__targetPath == other.targetPath
            and self.__partitionBy == other.partitionBy
        )
