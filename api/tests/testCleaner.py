import os
os.environ['ENV'] = 'TEST'
from helper.Cleaner import Cleaner
import unittest

"""
import debugpy
debugpy.listen(("0.0.0.0", 5678))
print("Waiting for client to attach...")
debugpy.wait_for_client()
"""

class CleanerTestCase(unittest.TestCase):
    """
    Test class for cleaner functionality
    """
    cleaner = Cleaner()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_convert_and_clean(self):
        sentence = """Datei-Speicherung.

Als Anwender soll der Datei-Speicherung Part-II zur Verfügung stehen, damit ich Ausgaben erhalte.

<h1>Weiter Informationen.</h1> <emph>Dateien immer erstellen.</emph> Die Erstellung ist sicherheitsrelevant. Siehe: https://test.com/sub

Akzeptanzkriterien:
- Fall-A
- Fall-B
-- Fall-BB
--- Fall-BB8
* Fall-C
** Fall-CC
# Fall-D
## Fall-DD

Anhänge:
A.pdf, B.pdf
"""
        expected = r"Datei-Speicherung. Als Anwender soll der Datei-Speicherung Part-II zur Verfügung stehen, damit ich Ausgaben erhalte. Weiter Informationen. Ausgaben immer erstellen. Die Datei-Erstellung ist sicherheitsrelevant. Siehe link Akzeptanzkriterien. Fall-A. Fall-B. Fall-BB. Fall-BB8. Fall-C. Fall-CC. Fall-D. Fall-DD. Anhänge A.pdf, B.pdf"
        cleaned_sentence = self.cleaner.convert_and_clean(sentence)
        self.assertEqual(cleaned_sentence, expected)

    def test_space_tokenizer_default(self):
        sentence = r"Datei-Speicherung. Als Anwender soll der Datei-Speicherung Part-II zur Verfügung stehen, damit ich Dateien erhalte. Weiter Informationen. Akzeptanzkriterien: Fall-A, Fall-B, Fall-C. A.pdf, B.pdf"
        expected = ['datei-speicherung', 'anwender', 'datei-speicherung', 'part-ii', 'verfügung', 'stehen', 'damit', 'dateien', 'erhalten', 'information', 'akzeptanzkriterie', \
                    'fall-a', 'fall-b', 'fall-c', 'a.pdf', 'b.pdf']

        cleaned_sentence = self.cleaner.spacy_tokenizer(sentence, remove_stop_words=True)

        self.assertEqual(cleaned_sentence, expected)

    def test_space_tokenizer_keep_stop_words(self):
        sentence = r"Datei-Speicherung. Als Anwender soll der Datei-Speicherung Part-II zur Verfügung stehen, damit ich Datein erhalte. Weiter Informationen. Akzeptanzkriterien: Fall-A, Fall-B, Fall-C. A.pdf, B.pdf"
        expected = [
            'datei-speicherung', 'als', 'anwender', 'sollen', 'der', 'datei-speicherung', 'part-ii', 'zu', 'verfügung', 'stehen', 'damit', 'dateien', 'erhalten', 'weiter', 'information', \
            'akzeptanzkriterie', 'fall-a', 'fall-b', 'fall-c', 'a.pdf', 'b.pdf']

        cleaned_sentence = self.cleaner.spacy_tokenizer(sentence, remove_stop_words=False)

        self.assertEqual(cleaned_sentence, expected)