from config.config_parser import config
import re
import spacy
from spacy.language import Language
from spacy.lang.de.stop_words import STOP_WORDS
from spacy.tokens import Token
import string

@Language.component("set_custom_boundaries")
def set_custom_boundaries(doc):
    '''
    Language Component sets rules for splitting sentences, used for the get_total_sentences function
    '''
    in_list = False

    for token in doc[:-1]:
        if doc[token.i].text in ("*", "#")\
        or re.search(r'^\-{1,}', doc[token.i].text):
            doc[token.i].is_sent_start = True
            in_list = True
        if re.search(r'\n{1,}', doc[token.i].text) and in_list:
            doc[token.i].is_sent_start = True
            in_list = False

    return doc

class Cleaner(object):
    '''
    Provides text cleaner and transformation methods to prepare text for nlp methods
    '''
    # https://explosion.ai/blog/german-model
    # Load German tokenizer, tagger, parser, NER and word vectors
    nlp = spacy.load(config['ai']['spacy_model'])
    # Add spacy step to convert listings to sentences
    nlp.add_pipe('set_custom_boundaries', before="parser")
    # Create our list of stopwords
    stop_words = STOP_WORDS
    # Drop predefined stop words to make these sensitive for model training
    stop_words -= {"möchte", "will", "um", "damit"}

    def is_valid_token(self, token: Token, check_stop_words: bool=True) -> bool:
        """
        Check if token is a valid word

        Args:
            token (Token): The token to check
            check_stop_words (bool): Check for stop words

        Returns:
            bool: True if token is valid, False otherwise
        """
        result = False

        if (not token.is_currency \
            and not token.is_digit \
            and not token.is_space \
            and not token.is_punct \
            and not token.like_num \
            and not token.pos_ == "PRON"):
            result = True

        # Check for stop words, if necessary
        if check_stop_words:
            result = result and not token.is_stop

        return result

    def spacy_tokenizer(self, sentence: str, remove_stop_words: bool=True) -> list:
        """
        Tokenize text with lemma transformation and cleaning options
        e.g., stops words, punctuations

        Args:
            sentence (str): The sentence to tokenize
            remove_stop_words (bool): Remove stop words

        Returns:
            list: The tokenized sentence
        """
        # Get cleaned tokens
        tokens = self.get_cleaned_spacy_tokens(sentence, remove_stop_words)

        # Lemmatization + remove special chars on left and right side
        tokens = [ token.lemma_.lower().strip(string.punctuation) for token in tokens ]

        return tokens

    def get_cleaned_spacy_tokens(self, sentence: str, remove_stop_words: bool=True) -> list:
        """
        Retrieve spacy tokens with cleaning

        Args:
            sentence (str): The sentence to tokenize
            remove_stop_words (bool): Remove stop words

        Returns:
            list: The cleaned tokens
        """
        # Creating doc object, which is used to create documents with linguistic annotations
        # Lemmatizing each token and converting it into lowercase
        doc = self.nlp(sentence)

        # Cleaning
        tokens = [ token for token in doc if self.is_valid_token(token, remove_stop_words) ]

        return tokens

    def is_valid_ner_token(self, token: Token) -> bool:
        """
        Check if token is part of a valid named entity

        Args:
            token (Token): The token to check

        Returns:
            bool: True if token is part of a named entity, False
        """
        return token.ent_iob_ in ('B', 'I')

    def get_cleaned_spacy_tokens_without_ner(
            self, sentence: str, remove_stop_words: bool=True) -> list:
        """
        Retrieve spacy tokens with basic cleaning and without named entities

        Args:
            sentence (str): The sentence to tokenize
            remove_stop_words (bool): Remove stop words

        Returns:
            list: The cleaned tokens
        """
        # Creating doc object, which is used to create documents with linguistic annotations
        # Lemmatizing each token and converting it into lowercase
        doc = self.nlp(sentence)

        # Basic cleaning + remove named entities
        tokens = [ token for token in doc if
                  self.is_valid_token(token, remove_stop_words) and
                  not self.is_valid_ner_token(token) ]

        return tokens

    def spacy_tokenizer_without_ner(self, sentence: str, remove_stop_words: bool=True) -> list:
        """
        Tokenize text with lemma transformation and cleaning options e.g.,
        stops words, punctuations. In addition, named entities are removed.

        Args:
            sentence (str): The sentence to tokenize
            remove_stop_words (bool): Remove stop words

        Returns:
            list: The tokenized sentence
        """
        # Cleaning
        tokens = self.get_cleaned_spacy_tokens_without_ner(sentence, remove_stop_words)

        # Lemmatization + remove special chars on left and right side
        tokens = [ token.lemma_.lower().strip(string.punctuation) for token in tokens ]

        return tokens

    def spacy_ner_tokenizer(self, sentence: str) -> list:
        """
        Extract named entities from a sentence

        Args:
            sentence (str): The sentence to tokenize

        Returns:
            list: The named entities
        """
        # Creating doc object, which is used to create documents with linguistic annotations
        doc = self.nlp(sentence)

        # Basic cleaning
        ners = [ ent.lemma_.lower().strip(string.punctuation) for ent in doc.ents ]

        return ners

    def convert_and_clean(self, text: str) -> str:
        """
        Convert listings to sentences and clean text

        Args:
            text (str): The text to convert and clean

        Returns:
            str: The cleaned text
        """
        text = self.clean_html(text)
        doc = self.nlp(text)
        sents = []
        for sent in list(doc.sents):
            text = self.clean(sent.text)
            if len(text) > 0:
                sents.append(text)

        text = ". ".join(sents)
        text = self.check_punct(text)

        return text

    def clean_html(self, text: str) -> str:
        """
        Remove html tags and links from text

        Args:
            text: The text to clean

        Returns:
            Cleaned text
        """
        # Remove HTML tags but keep their contents
        text = re.sub(r'<.*?>', r' ', text)

        # Replace all links with "link" to keep the link info as additional info in the document
        text = re.sub(r"https?://\S+", r'link', text)

        # Remove html elements like &nbsp;
        text = re.sub(r'&(.*?);', r' ', text)

        return text

    def clean(self, text: str) -> str:
        """
        Remove extra spaces, tabs, and line breaks

        Args:
            text (str): The text to clean

        Returns:
            str: The cleaned text
        """
        # Convert new lines to dots
        text = re.sub(r'(\w+)\n', r'\1. ', text)

        # https://dylancastillo.co/nlp-snippets-clean-and-tokenize-text-with-python/#remove-hyperlinks
        text = " ".join(text.split())

        # Clean text from HTML tags and links
        text = self.clean_html(text)

        # Remove punctuation
        remove = string.punctuation
        remove = re.sub(r'[\,\.\-\_]',r'', remove) # keep a couple of special chars to prevent sentence structure.
        text = re.sub(f"[{re.escape(remove)}]", r'', text)

        # Remove repeated punctuations
        text = re.sub(f"[{re.escape(string.punctuation)}]{{2,}}", r'', text)

        # Remove any repeated characters (e.g., aaa -> a)
        text = re.sub(r'(.)\1{2,}',r'\1', text)

        # Remove short tokens (fast approach)
        tokens = text.split()
        clean_tokens = [t for t in tokens if len(t) > 1]
        text = " ".join(clean_tokens)

        # Remove dot(s) at sentence end to prevent multi dots
        text = text.rstrip(r'.')

        return text

    def check_punct(self, text: str) -> str:
        """
        Helper method to complete sentence with final dots
        to allow sentence detecting in nlp processes.

        Args:
            text (str): The text to check

        Returns:
            str: The text with final dot
        """
        if len(text.strip()) != 0 and not re.match(r'.*\.$', text):
            text += "."

        return text
       