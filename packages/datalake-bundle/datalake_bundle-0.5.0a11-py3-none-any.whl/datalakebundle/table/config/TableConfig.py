# pylint: disable = too-many-instance-attributes
import json


class TableConfig:

    def __init__(
        self,
        identifier: str,
        dbIdentifier: str,
        dbName: str,
        tableIdentifier: str,
        tableName: str,
        schemaPath: str,
        targetPath: str,
        notebookPath: str,
        partitionBy: list = None,
        **kwargs,
    ):
        self.__identifier = identifier
        self.__dbIdentifier = dbIdentifier
        self.__dbName = dbName
        self.__tableIdentifier = tableIdentifier
        self.__tableName = tableName
        self.__schemaPath = schemaPath
        self.__targetPath = targetPath
        self.__notebookPath = notebookPath
        self.__partitionBy = partitionBy or []
        self.__customFields = kwargs

    @property
    def identifier(self):
        return self.__identifier

    @property
    def dbIdentifier(self):
        return self.__dbIdentifier

    @property
    def dbName(self):
        return self.__dbName

    @property
    def tableIdentifier(self):
        return self.__tableIdentifier

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
    def notebookPath(self):
        return self.__notebookPath

    @property
    def partitionBy(self):
        return self.__partitionBy

    @property
    def fullTableName(self):
        return self.__dbName + '.' + self.__tableName

    def getCustomFields(self):
        return self.__customFields

    def asDict(self):
        return {**self.__customFields, **{
            'identifier': self.__identifier,
            'dbIdentifier': self.__dbIdentifier,
            'dbName': self.__dbName,
            'tableIdentifier': self.__tableIdentifier,
            'tableName': self.__tableName,
            'schemaPath': self.__schemaPath,
            'targetPath': self.__targetPath,
            'notebookPath': self.__notebookPath,
            'partitionBy': self.__partitionBy,
        }}

    def __getattr__(self, item):
        if item not in self.__customFields:
            raise Exception(f'Unexpected attribute: "{item}"')

        return self.__customFields[item]

    def __eq__(self, other: 'TableConfig'):
        return self.asDict() == other.asDict()

    def __repr__(self):
        return json.dumps(self.asDict(), indent=4)
