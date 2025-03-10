import os
os.environ['ENV'] = 'TEST'
from config.config_parser import config
from metrics.metrics import Metrics
import shutil
import unittest

class P1UserTestCase(unittest.TestCase):
    """
    Test class for user functionality
    """
    project = "p1"
    m = Metrics(
        project=project,
        user_story="""Datei-Speicherung.

Als Benutzer will ich, dass die Datei-Speicherung Part-II zur Verfügung steht, damit ich Dateien erhalte.

<h1>Weiter Informationen.</h1> <emph>Dateien immer erstellen.</emph> Die Datei-Erstellung ist sicherheitsrelevant. Siehe: https://test.com/sub

Akzeptanzkriterien:
- Fall-A
- Fall-B
- Fall-C

Anhänge:
A.pdf, B.pdf
""")

    def tearDown(self):
        """
        Cleanup files
        """
        cache_patch = config['test']['cache_path']
        for file_name in os.listdir(cache_patch):
            file = cache_patch + '/' + file_name
            if os.path.isfile(file):
                os.remove(file)
            else:
                shutil.rmtree(file)

    def test_format_complete(self):
        """
        Test format complete metric
        """
        expected = 0.8333333333333334
        fc = self.m.get_metric('format_complete')
        output = fc.run()

        self.assertEqual(output, expected)

    def test_train_format_complete(self):
        """
        Test train format complete
        """
        fc = self.m.get_metric('format_complete')
        # Format complete variables
        meta = fc.format_complete_meta
        self.assertEqual(
            {'title': {'acc_mean': 0.9, 'acc_std': 0.20000000000000004, 'acc': 1.0},
             'persona': {'acc_mean': 0.9, 'acc_std': 0.20000000000000004, 'acc': 1.0},
             'what': {'acc_mean': 0.9, 'acc_std': 0.20000000000000004, 'acc': 1.0},
             'why': {'acc_mean': 0.9, 'acc_std': 0.20000000000000004, 'acc': 1.0},
             'acceptance_criteria': {'acc_mean': 0.9, 'acc_std': 0.20000000000000004, 'acc': 1.0},
             'attachments': {'acc_mean': 0.9, 'acc_std': 0.20000000000000004, 'acc': 1.0}}, meta)

    def test_readable(self):
        """
        Test readable metric
        """
        expected = 0.15722222222222224
        r = self.m.get_metric('readable')
        output = r.run()

        self.assertEqual(output, expected)

    def test_customer_speak(self):
        """
        Test customer speak metric"
        """
        expected = 0.13636363636363635
        cs = self.m.get_metric('customer_speak')
        output = cs.run()

        self.assertEqual(output, expected)

    def test_small(self):
        """
        Test small metric
        """
        expected = 0
        s = self.m.get_metric('small')
        output = s.run()

        self.assertEqual(output, expected)

    def test_independent(self):
        """
        Test independent metric
        """
        expected = 0.17618454063816402
        i = self.m.get_metric('independent')
        output = i.run()

        self.assertEqual(output, expected)

    def test_word_sparse(self):
        """
        Test word sparse metric
        """
        expected = 0.9396551724137931
        ws = self.m.get_metric('word_sparse')
        output = ws.run()

        self.assertEqual(output, expected)

    def test_sentence_sparse(self):
        """
        Test sentence sparse metric
        """
        expected = 0.3333333333333333
        ssp = self.m.get_metric('sentence_sparse')
        output = ssp.run()

        self.assertEqual(output, expected)

    def test_easy_language(self):
        """
        Test easy language metric
        """
        expected = 0.3103448275862069
        el = self.m.get_metric('easy_language')
        output = el.run()

        self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()
