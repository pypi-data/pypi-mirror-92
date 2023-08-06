import unittest
from datalakebundle.table.config.FieldsResolver import FieldsResolver

class FieldsResolverTest(unittest.TestCase):

    def setUp(self) -> None:
        self.__fieldsResolver = FieldsResolver()

    def test_basic(self):
        result = self.__fieldsResolver.resolve(
            {
                'identifier': 'mydatabase.my_table',
                'dbIdentifier': 'mydatabase',
                'tableIdentifier': 'my_table',
                'schemaPath': 'datalakebundle.test.mydatabase.my_table.schema',
            },
            {
                'schemaPath': 'datalakebundle.test.{dbIdentifier}.{tableIdentifier}.schema',
                'targetPath': {
                    'resolverClass': 'datalakebundle.test.SimpleTargetPathResolver',
                    'resolverArguments': [
                        '/foo/bar'
                    ],
                }
            }
        )

        self.assertEqual({
            'identifier': 'mydatabase.my_table',
            'dbIdentifier': 'mydatabase',
            'tableIdentifier': 'my_table',
            'schemaPath': 'datalakebundle.test.mydatabase.my_table.schema',
            'targetPath': '/foo/bar/mydatabase/my_table.delta',
        }, result)


    def test_explicitOverridingDefaults(self):
        result = self.__fieldsResolver.resolve(
            {
                'identifier': 'mydatabase.my_table',
                'dbIdentifier': 'mydatabase',
                'tableIdentifier': 'my_table',
                'schemaPath': 'datalakebundle.test.mydatabase.my_table.schema2',
                'targetPath': '/foo/bar/mydatabase/my_table_new.delta',
            },
            {
                'schemaPath': 'datalakebundle.test.{dbIdentifier}.{tableIdentifier}.schema',
                'targetPath': {
                    'resolverClass': 'datalakebundle.test.SimpleTargetPathResolver',
                    'resolverArguments': [
                        '/foo/bar'
                    ],
                }
            }
        )

        self.assertEqual({
            'dbIdentifier': 'mydatabase',
            'tableIdentifier': 'my_table',
            'identifier': 'mydatabase.my_table',
            'schemaPath': 'datalakebundle.test.mydatabase.my_table.schema2',
            'targetPath': '/foo/bar/mydatabase/my_table_new.delta',
        }, result)

if __name__ == '__main__':
    unittest.main()
