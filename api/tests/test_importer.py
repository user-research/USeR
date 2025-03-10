import os
os.environ['ENV'] = 'TEST'
from config.config_parser import config
from importer.p1_importer import P1Importer
import unittest

class P1ImporterTestCase(unittest.TestCase):
    """
    Test class for importer functionality
    """
    project = "p1"
    original_backlog_file = config['project']['backlog_file']

    def setUp(self):
        """
        Setup the test case
        """
        config['project']['backlog_file'] = config['test']['backlog_test_file']

    def tearDown(self):
        """
        Cleanup files
        """
        os.remove(
            config['project']['backlog_file'].format(project=self.project)
        )
        config['project']['backlog_file'] = self.original_backlog_file

    def test_import(self):
        """
        Test import function
        """
        p = P1Importer()
        p.import_backlog()
        self.assertTrue(
            os.path.isfile(config['project']['backlog_file'].format(project=self.project)))

if __name__ == '__main__':
    unittest.main()
