import os
os.environ['ENV'] = 'TEST'
from config.user.UserConfigParser import config
from metrics.Metrics import Metrics
import shutil
import unittest

"""
import debugpy
debugpy.listen(("0.0.0.0", 5678))
print("Waiting for client to attach...")
debugpy.wait_for_client()
"""

class UserTestCase(unittest.TestCase):
    """
    Test class for user functionality
    """
    project = "p1"

    m = Metrics(
        project=project,
        user_story=r"""Datei-Speicherung.

Als Anwender soll der Datei-Speicherung Part-II zur Verfügung stehen, damit ich Dateien erhalte.

<h1>Weiter Informationen.</h1> <emph>Dateis immer erstellen.</emph> Die Datei-Erstellung ist sicherheitsrelevant. Siehe: https://test.com/sub

Akzeptanzkriterien:
- Fall-A
- Fall-B
- Fall-C

Anhänge:
A.pdf, B.pdf
""")

    def tearDown(self):
        '''
        Cleanup files
        '''
        cache_patch = config['test']['cache_path']
        for file_name in os.listdir(cache_patch):
            file = cache_patch + '/' + file_name
            if os.path.isfile(file):
                os.remove(file)
            else:
                shutil.rmtree(file)

    def test_format_complete(self):
        expected = 0.0
        fc = self.m.get_metric('format_complete')
        output = fc.run()

        self.assertEqual(output, expected)
    
    ### Failes in init/demo mode, because of the small p1 dataset, so meta data is empty {} ###
    def test_train_format_complete(self):
        fc = self.m.get_metric('format_complete')
        # Format complete variables
        meta = fc.format_complete_meta
        self.assertEqual( 
            {'title': {'acc_mean': 0.9199999999999999, 'acc_std': 0.09797958971132709, 'acc': 1.0},
             'persona': {'acc_mean': 0.74, 'acc_std': 0.14628738838327796, 'acc': 1.0},
             'what': {'acc_mean': 0.72, 'acc_std': 0.1691153452528776, 'acc': 1.0},
             'why': {'acc_mean': 0.5900000000000001, 'acc_std': 0.18275666882497066, 'acc': 0.75},
             'acceptance_criteria': {'acc_mean': 0.9, 'acc_std': 0.2, 'acc': 1.0},
             'additionals': {'acc_mean': 0.82, 'acc_std': 0.1833030277982336, 'acc': 1.0},
             'attachments': {'acc_mean': 0.8699999999999999, 'acc_std': 0.10770329614269006, 'acc': 1.0}}, meta)

    def test_readable(self):
        expected = 0.16055555555555553
        r = self.m.get_metric('readable')
        output = r.run()

        self.assertEqual(output, expected)

    def test_customer_speak(self):
        expected = 0.09090909090909091
        cs = self.m.get_metric('customer_speak')
        output = cs.run()

        self.assertEqual(output, expected)

    def test_small(self):
        expected = 0
        s = self.m.get_metric('small')
        output = s.run()

        self.assertEqual(output, expected)

    def test_independent(self):
        expected = 0.21484815322867878
        i = self.m.get_metric('independent')
        output = i.run()

        self.assertEqual(output, expected)

    def test_word_sparse(self):
        expected = 0.5102040816326531
        ws = self.m.get_metric('word_sparse')
        output = ws.run()

        self.assertEqual(output, expected)

    def test_sentence_sparse(self):
        expected = 0.14285714285714285
        ssp = self.m.get_metric('sentence_sparse')
        output = ssp.run()

        self.assertEqual(output, expected)

    def test_easy_language(self):
        expected = 0.3103448275862069
        el = self.m.get_metric('easy_language')
        output = el.run()

        self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()
