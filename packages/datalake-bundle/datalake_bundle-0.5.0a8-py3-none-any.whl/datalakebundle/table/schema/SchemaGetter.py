import pyspark.sql.types as T
import importlib
from databricksbundle.help import htmlHelpers
from databricksbundle.help.HtmlDescriptionProvider import HtmlDescriptionProvider

class SchemaGetter(HtmlDescriptionProvider):

    def get(self, schemaPath: str) -> T.StructType:
        getSchema = getattr(importlib.import_module(schemaPath), 'getSchema')

        return getSchema()

    def getHtmlDescription(self):
        return htmlHelpers.code("get(schemaPath)")
