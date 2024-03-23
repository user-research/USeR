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
    original_corpus_file = config['project']['corpus_file']

    def setUp(self):
        config['project']['corpus_file'] = config['test']['corpus_test_file']

    def tearDown(self):
        '''
        Cleanup files
        '''
        os.remove(
            config['project']['corpus_file'].format(project=self.project)
        )
        config['project']['corpus_file'] = self.original_corpus_file

    def test_import(self):
        p = P1Importer()
        p.import_corpus()
        self.assertTrue(
            os.path.isfile(config['project']['corpus_file'].format(project=self.project)))

if __name__ == '__main__':
    unittest.main()