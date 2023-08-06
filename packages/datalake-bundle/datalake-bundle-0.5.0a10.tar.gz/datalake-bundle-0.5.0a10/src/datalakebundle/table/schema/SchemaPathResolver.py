from box import Box
from datalakebundle.table.identifier.ValueResolverInterface import ValueResolverInterface

class SchemaPathResolver(ValueResolverInterface):

    def resolve(self, rawTableConfig: Box):
        notebookPath = rawTableConfig['notebookPath']

        return notebookPath[:notebookPath.rfind('.')] + '.schema'

    def getDependingFields(self) -> set:
        return {'notebookPath'}
