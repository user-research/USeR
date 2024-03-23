import os
os.environ['ENV'] = 'TEST'
from config.user.UserConfigParser import config
from importer.P1Importer import P1Importer
import unittest

"""
import debugpy
debugpy.listen(("0.0.0.0", 5678))
print("Waiting for client to attach...")
debugpy.wait_for_client()
"""

class ImporterTestCase(unittest.TestCase):
    """
    Test class for importer functionality
    """
    project = "p1"
    original_backlog_file = config['project']['backlog_file']

    def setUp(self):
        config['project']['backlog_file'] = config['test']['backlog_test_file']

    def tearDown(self):
        '''
        Cleanup files
        '''
        os.remove(
            config['project']['backlog_file'].format(project=self.project)
        )
        config['project']['backlog_file'] = self.original_backlog_file

    def test_import(self):
        p = P1Importer()
        p.import_backlog()
        self.assertTrue(
            os.path.isfile(config['project']['backlog_file'].format(project=self.project)))

if __name__ == '__main__':
    unittest.main()