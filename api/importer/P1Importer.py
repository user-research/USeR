import pandas as pd

from importer.Importer import Importer

class P1Importer(Importer):
    project = "p1"

    def __init__(self):
        super().__init__(self.project)

    def import_corpus(self):
        corpus = []

        # Map project export csv fields to standardized tool fields
        for _, story in self.raw_corpus.iterrows():
            text = self.cleaner.convert_and_clean(story.Text)
            attachments = story.Attachments

            patterns = []

            for pattern in [text, attachments]:
                if len(pattern) > 0:
                    pattern = self.cleaner.check_punct(pattern)
                    patterns.append(pattern)

            text = ' '.join(patterns)
            
            corpus.append({
                'usid': story.Key,
                'text': text,
                
                # Labels
                'title_label': story['Has.Title'],
                'persona_label': story['Has.Persona'],
                'what_label': story['Has.What'],
                'why_label': story['Has.Why'],
                'acceptance_criteria_label': story['Has.Acceptance.Criteria'],
                'additionals_label': story['Has.Additionals'],
                'attachments_label': story['Has.Attachments']})

        

        self.corpus = pd.DataFrame(corpus)
        pd.DataFrame(self.corpus).to_csv(self.corpus_file, index=False)