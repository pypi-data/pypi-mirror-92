import unittest
from datalakebundle.table.config.TableConfig import TableConfig
from datalakebundle.table.config.TableConfigParser import TableConfigParser

class TableConfigParserTest(unittest.TestCase):

    def setUp(self):
        self.__tableConfigParser = TableConfigParser('test_{identifier}')

    def test_basic(self):
        result = self.__tableConfigParser.parse(
            'mydatabase.my_table', {
                'schemaPath': 'datalakebundle.test.TestSchema',
                'targetPath': '/foo/bar/mydatabase/my_table.delta',
                'notebookPath': '/foo/mydatabase/my_table/my_table.py',
                'partitionBy': 'mycolumn',
            }
        )

        self.assertEqual(TableConfig(**{
            'dbIdentifier': 'mydatabase',
            'tableIdentifier': 'my_table',
            'identifier': 'mydatabase.my_table',
            'dbName': 'test_mydatabase',
            'tableName': 'my_table',
            'schemaPath': 'datalakebundle.test.TestSchema',
            'targetPath': '/foo/bar/mydatabase/my_table.delta',
            'notebookPath': '/foo/mydatabase/my_table/my_table.py',
            'partitionBy': ['mycolumn'],
        }), result)

    def test_defaultsOnly(self):
        result = self.__tableConfigParser.parse(
            'mydatabase.my_table', {}, {
                'schemaPath': 'datalakebundle.test.{dbIdentifier}.{tableIdentifier}.schema',
                'targetPath': {
                    'resolverClass': 'datalakebundle.test.SimpleTargetPathResolver',
                    'resolverArguments': [
                        '/foo/bar'
                    ],
                },
                'notebookPath': '/foo/{dbIdentifier}/{tableIdentifier}/{tableIdentifier}.py'
            }
        )

        self.assertEqual(TableConfig(**{
            'dbIdentifier': 'mydatabase',
            'tableIdentifier': 'my_table',
            'identifier': 'mydatabase.my_table',
            'dbName': 'test_mydatabase',
            'tableName': 'my_table',
            'schemaPath': 'datalakebundle.test.mydatabase.my_table.schema',
            'targetPath': '/foo/bar/mydatabase/my_table.delta',
            'notebookPath': '/foo/mydatabase/my_table/my_table.py'
        }), result)

    def test_explicitOverridingDefaults(self):
        result = self.__tableConfigParser.parse(
            'mydatabase.my_table', {
                'schemaPath': 'datalakebundle.test.mydatabase.my_table.schema2',
                'partitionBy': ['mycolumn']
            }, {
                'schemaPath': 'datalakebundle.test.{dbIdentifier}.{tableIdentifier}.schema',
                'targetPath': {
                    'resolverClass': 'datalakebundle.test.SimpleTargetPathResolver',
                    'resolverArguments': [
                        '/foo/bar'
                    ],
                },
                'notebookPath': '/foo/{dbIdentifier}/{tableIdentifier}/{tableIdentifier}.py'
            }
        )

        self.assertEqual(TableConfig(**{
            'dbIdentifier': 'mydatabase',
            'tableIdentifier': 'my_table',
            'identifier': 'mydatabase.my_table',
            'dbName': 'test_mydatabase',
            'tableName': 'my_table',
            'schemaPath': 'datalakebundle.test.mydatabase.my_table.schema2',
            'targetPath': '/foo/bar/mydatabase/my_table.delta',
            'notebookPath': '/foo/mydatabase/my_table/my_table.py',
            'partitionBy': ['mycolumn'],
        }), result)

if __name__ == '__main__':
    unittest.main()
