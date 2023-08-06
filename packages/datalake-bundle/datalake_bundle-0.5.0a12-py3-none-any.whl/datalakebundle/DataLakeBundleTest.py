import unittest
from injecta.testing.servicesTester import testServices
from pyfonycore.bootstrap import bootstrappedContainer
from datalakebundle.table.config.TableConfig import TableConfig
from datalakebundle.table.config.TableConfigManager import TableConfigManager

class DataLakeBundleTest(unittest.TestCase):

    def setUp(self):
        self._container = bootstrappedContainer.init('test')
        self.maxDiff = 8000*8

    def test_init(self):
        testServices(self._container)

    def test_tableConfigs(self):
        tableConfigManager: TableConfigManager = self._container.get(TableConfigManager)

        myTableConfig = tableConfigManager.get('mydatabase_e.my_table')
        anotherTableConfig = tableConfigManager.get('mydatabase_p.another_table')

        self.assertEqual(TableConfig(**{
            'schemaPath': 'datalakebundle.test.TestSchema',
            'dbIdentifier': 'mydatabase_e',
            'tableIdentifier': 'my_table',
            'identifier': 'mydatabase_e.my_table',
            'notebookPath': 'datalakebundle.mydatabase_e.my_table.my_table',
            'dbName': 'test_mydatabase_e',
            'tableName': 'my_table',
            'encrypted': True,
            'dbIdentifierBase': 'mydatabase',
            'targetPath': '/foo/bar/mydatabase/encrypted/my_table.delta',
        }), myTableConfig)

        self.assertEqual(TableConfig(**{
            'schemaPath': 'datalakebundle.test.AnotherSchema',
            'partitionBy': ['date'],
            'dbIdentifier': 'mydatabase_p',
            'tableIdentifier': 'another_table',
            'notebookPath': 'datalakebundle.mydatabase_p.another_table.another_table',
            'identifier': 'mydatabase_p.another_table',
            'dbName': 'test_mydatabase_p',
            'tableName': 'another_table',
            'encrypted': False,
            'dbIdentifierBase': 'mydatabase',
            'targetPath': '/foo/bar/mydatabase/plain/another_table.delta',
        }), anotherTableConfig)

if __name__ == '__main__':
    unittest.main()
