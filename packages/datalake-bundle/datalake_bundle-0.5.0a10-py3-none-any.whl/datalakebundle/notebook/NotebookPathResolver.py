import string
from box import Box
from datalakebundle.table.identifier.ValueResolverInterface import ValueResolverInterface

class NotebookPathResolver(ValueResolverInterface):

    def __init__(
        self,
        notebookPathTemplate: str,
        rootModuleName: str,
    ):
        self.__notebookPathTemplate = notebookPathTemplate
        self.__rootModuleName = rootModuleName

    def resolve(self, rawTableConfig: Box):
        replacements = rawTableConfig
        replacements['rootModulePath'] = self.__rootModuleName

        path = self.__notebookPathTemplate.format(**replacements)

        return path.rstrip('.py').replace('/', '.')

    def getDependingFields(self) -> set:
        fields = self.__parsePlacelhoders()

        if 'rootModulePath' in fields:
            fields.remove('rootModulePath')

        return fields

    def __parsePlacelhoders(self):
        iterator = string.Formatter().parse(self.__notebookPathTemplate)

        return {name for text, name, spec, conv in iterator if name is not None}
