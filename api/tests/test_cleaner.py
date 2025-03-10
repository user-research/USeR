import os
os.environ['ENV'] = 'TEST'
from helper.cleaner import Cleaner
import unittest

class P1CleanerTestCase(unittest.TestCase):
    """
    Test class for cleaner functionality
    """
    cleaner = Cleaner()

    def test_convert_and_clean(self):
        """
        Test convert and clean function
        """
        sentence = """Datei-Speicherung.

Als Benutzer will ich, dass die Datei-Speicherung Part-II zur Verfügung steht, damit ich Ausgaben erhalte.

<h1>Weiter Informationen.</h1> Dateien immer erstellen. Die Erstellung ist sicherheitsrelevant. Siehe: https://test.com/sub

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
        expected = "Datei-Speicherung. Als Benutzer will ich, dass die Datei-Speicherung Part-II zur Verfügung steht, damit ich Ausgaben erhalte. Weiter Informationen. Dateien immer erstellen. Die Erstellung ist sicherheitsrelevant. Siehe link. Akzeptanzkriterien. Fall-A. Fall-B. Fall-BB. Fall-BB8. Fall-C. Fall-CC. Fall-D. Fall-DD. Anhänge A.pdf, B.pdf."
        cleaned_sentence = self.cleaner.convert_and_clean(sentence)
        self.assertEqual(cleaned_sentence, expected)

    def test_space_tokenizer_default(self):
        """
        Test space tokenizer with default settings
        """
        sentence = "Datei-Speicherung. Als Benutzer will ich, dass die Datei-Speicherung Part-II zur Verfügung steht, damit ich Dateien erhalte. Weiter Informationen. Akzeptanzkriterien: Fall-A, Fall-B, Fall-C. A.pdf, B.pdf"
        expected = ['datei-speicherung', 'benutzer', 'wollen', 'datei-speicherung', 'part-ii',
                    'verfügung', 'stehen', 'damit', 'datei', 'erhalten', 'information',
                    'akzeptanzkriterie', 'fall-a', 'fall-b', 'fall-c', 'a.pdf', 'b.pdf']

        cleaned_sentence = self.cleaner.spacy_tokenizer(sentence, remove_stop_words=True)

        self.assertEqual(cleaned_sentence, expected)

    def test_space_tokenizer_keep_stop_words(self):
        """
        Test space tokenizer with keep stop words
        """
        sentence = "Datei-Speicherung. Als Benutzer will ich, dass die Datei-Speicherung Part-II zur Verfügung steht, damit ich Dateien erhalte. Weitere Informationen. Akzeptanzkriterien: Fall-A, Fall-B, Fall-C. A.pdf, B.pdf"
        expected = [
            'datei-speicherung', 'als', 'benutzer', 'wollen', 'dass', 'der', 'datei-speicherung',
            'part-ii', 'zu', 'verfügung', 'stehen', 'damit', 'datei', 'erhalten', 'weit',
            'information', 'akzeptanzkriterie', 'fall-a', 'fall-b', 'fall-c', 'a.pdf', 'b.pdf']

        cleaned_sentence = self.cleaner.spacy_tokenizer(sentence, remove_stop_words=False)

        self.assertEqual(cleaned_sentence, expected)

if __name__ == '__main__':
    unittest.main()
