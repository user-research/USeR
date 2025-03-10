import pandas as pd
from importer.base_importer import Importer

class P1Importer(Importer):
    """
    P1Importer class
    """
    project = "p1"

    def __init__(self):
        """
        Initialize the P1 importer class
        """
        super().__init__(self.project)
        self.backlog = pd.DataFrame()

    def import_backlog(self):
        """
        Import the project backlog
        """
        backlog = []

        # Map project export csv fields to standardized tool fields
        for _, story in self.raw_backlog.iterrows():
            title = self.cleaner.clean(story.title)
            description = self.cleaner.convert_and_clean(story.description)
            acceptance_criteria = self.cleaner.convert_and_clean(story.acceptance_criteria)
            attachments = story.attachments

            patterns = []

            for pattern in [title, description, acceptance_criteria, attachments]:
                if len(pattern) > 0:
                    pattern = self.cleaner.check_punct(pattern)
                    patterns.append(pattern)

            text = ' '.join(patterns)

            # Mandatory fields see ./api/importer/base_importer.py: Importer.import_backlog()
            backlog.append({
                'usid': story.key,
                'text': text,

                # Labels
                'title_label': story['has_title'],
                'persona_label': story['has_persona'],
                'what_label': story['has_what'],
                'why_label': story['has_why'],
                'acceptance_criteria_label': story['has_acceptance_criteria'],
                'attachments_label': story['has_attachments']})

        self.backlog = pd.DataFrame(backlog)
        pd.DataFrame(self.backlog).to_csv(self.backlog_file, index=False)
