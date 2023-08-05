from box import Box
from datalakebundle.table.config import primitiveValue
from datalakebundle.table.config.ValueResolverFactory import ValueResolverFactory
from datalakebundle.table.identifier.fillTemplate import fillTemplate
from datalakebundle.table.identifier.IdentifierParser import IdentifierParser

class TableConfigParser:

    def __init__(
        self,
        tableNameTemplate: str
    ):
        self.__valueResolverFactory = ValueResolverFactory()
        self.__identifierParser = IdentifierParser()
        self.__tableNameTemplate = tableNameTemplate

    def parse(self, identifier: str, explicitConfig: dict, defaults: dict = None):
        defaults = defaults or dict()
        identifiers = self.__identifierParser.parse(identifier)
        tableNameParts = self.__resolveTableNameParts(identifiers)

        allFields = {**identifiers, **tableNameParts, **explicitConfig}

        for name, val in self.__filterPrimitive(allFields, defaults).items():
            allFields[name] = primitiveValue.evaluate(val, allFields)

        return self.__resolve(allFields, defaults)

    def __resolve(self, allFields: dict, defaults: dict):
        resolverKeys = [name for name, val in defaults.items() if isinstance(val, dict) and name not in allFields]

        while resolverKeys:
            name = resolverKeys.pop(0)
            resolver = self.__valueResolverFactory.create(defaults[name])
            dependentFields = resolver.getDependingFields()

            if dependentFields - set(allFields.keys()) == set():
                allFields[name] = resolver.resolve(Box(allFields))
            else:
                resolverKeys.append(name)

        return allFields

    def __filterPrimitive(self, allFields: dict, defaults: dict):
        return {name: val for name, val in defaults.items() if not isinstance(val, dict) and name not in allFields}

    def __resolveTableNameParts(self, identifiers: dict):
        fullTableName = fillTemplate(self.__tableNameTemplate, identifiers)
        dotPosition = fullTableName.find('.')

        if dotPosition == -1:
            raise Exception('Table name must meet the following format: {dbName}.{tableName}')

        return {
            'dbName': fullTableName[:dotPosition],
            'tableName': fullTableName[dotPosition + 1:],
        }
