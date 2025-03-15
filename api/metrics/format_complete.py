from metrics.base_metric import BaseMetric, config, logging
from numpy import mean, std
import os
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

class FormatComplete(BaseMetric):
    """
    Metric class: format complete
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the format complete metric class

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)

        # Reset project var in context of format complete metric which works across projects
        self.project = ""

        # User story format fields, we need to select the lable data in the backlog
        self.fields = config['app']['fields'].split(r',')

        # Format complete variables
        self.estimators = {}

        self.format_complete_meta = {}

        # Store models for format_complete quality predictions
        self.form_field_predictions = {}

        # Quality metrics
        self._format_complete = 0.0

        # Init format complete training
        for field in self.fields:
            try:
                self._train_format_complete(field)
            except ValueError as e:
                logging.error('Failure in training SVN model: %s', e)

    def run(self):
        """
        Runs the metrics calculation

        Returns:
            float: The format complete metric
        """
        return self.format_complete()

    def get_vocabulary(self, field):
        """
        Get the vocabulary of a field

        Args:
            field (str): The field name

        Returns:
            dict: The vocabulary
        """
        return self.estimators[field]['vectorizer'].vocabulary_

    def get_vocabulary_len(self):
        """
        Get the vocabulary length of all fields

        Returns:
            dict: The vocabulary length
        """
        length = {}
        for field in self.fields:
            length[field] = len(self.get_vocabulary(field))

        return length

    def get_documents_length(self):
        """
        Get the length of all documents

        Returns:
            int: The length of all documents
        """
        return len(pd.concat(self.backlogs.get_all()))

    def get_form_field_predictions(self) -> dict:
        """
        Get the form field predictions

        Returns:
            dict: The form field predictions
        """
        return self.predict_form_fields()

    def get_format_complete_meta(self) -> dict:
        """
        Get the format complete meta data

        Returns:
            dict: The format complete
        """
        return self.format_complete_meta

    def _train_format_complete(self, field: str="persona"):
        """
        Train method to setup the predictions SVM models

        Args:
            field (str): The field name
        """
        tmp_backlogs = pd.concat(self.backlogs.get_all())
        x = tmp_backlogs['text'].to_numpy()
        y = tmp_backlogs[field+'_label'].to_numpy()

        cache_file = config['global']['format_complete_file'].format(field=field)

        if os.path.exists(cache_file):
            with open(cache_file, "rb") as fh:
                best = pickle.load(fh)
        else:
            # https://machinelearningmastery.com/nested-cross-validation-for-machine-learning-with-python/
            # Configure the cross-validation procedure
            skf = StratifiedKFold(n_splits=5)

            # Enumerate splits
            best = {}
            acc_results = []

            for train_ix, test_ix in skf.split(x, y):

                # Split data
                x_train, x_test = x[train_ix], x[test_ix]
                y_train, y_test = y[train_ix], y[test_ix]

                # Vectorizer
                tfidf_vector = TfidfVectorizer(tokenizer=self._spacy_tokenizer)

                # Using Support Vector Machine as predictor
                classifier = SVC(C=1.0, degree=3, gamma='scale', kernel='linear')

                # Create pipeline using TF-IDF
                pipe = Pipeline([
                    ('vectorizer', tfidf_vector),
                    ('classifier', classifier)])

                pipe.fit(x_train, y_train)

                # Evalute model on the hold out dataset
                yhat = pipe.predict(x_test)
                # Evalute the model
                acc = accuracy_score(y_test, yhat)
                acc_results.append(acc)

                # Report progress
                print(f'>train SVC: field={field}, acc={acc:.3f}')

                # Save best estimator
                if ('acc' not in best) or (acc > best['acc']):
                    best['estimator'] = pipe
                    best['acc'] = acc

            # Summarize the estimated performance of the model
            best['acc_mean'] = mean(acc_results)
            best['acc_std'] = std(acc_results)

            print(f"Accuracy: {best['acc_mean']:.3f} ({best['acc_std']:.3f})")

            with open(cache_file, "wb") as fh:
                pickle.dump(best, fh)

        self.estimators[field] = best['estimator']
        self.format_complete_meta[field] = {
            'acc_mean':best['acc_mean'],
            'acc_std':best['acc_std'],
            'acc':best['acc']}

    def predict_form_fields(self) -> dict:
        """ 
        Predict new user story whether the form fields are present or not

        Returns:
            dict: The form field predictions
        """
        # Predict presence of form fields
        for field in self.fields:
            try:
                self.form_field_predictions[field] = \
                    self.estimators[field].predict([self.user_story])[0]
            except KeyError as e:
                logging.error(e)

        return self.form_field_predictions

    def format_complete(self) -> float:
        """
        Calculates the format_complete quality index
        
        Returns:
            The number of filled form fields as percentage e.g. 0.3
        """
        self._format_complete = sum(self.get_form_field_predictions().values())
        self._format_complete = self._format_complete / len(self.fields)

        return self._format_complete
