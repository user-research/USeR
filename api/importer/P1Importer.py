import pandas as pd

from importer.Importer import Importer

class P1Importer(Importer):
    project = "p1"

    def __init__(self):
        super().__init__(self.project)

    def import_backlog(self):
        backlog = []

        # Map project export csv fields to standardized tool fields
        for _, story in self.raw_backlog.iterrows():
            shortname = story.Shortname
            summary = self.cleaner.clean(story.Summary)
            description = self.cleaner.convert_and_clean(story.Description)
            acceptance_criteria = self.cleaner.convert_and_clean(story.Akzeptanzkriterien)
            attachments = story.Attachment

            patterns = []

            for pattern in [shortname, summary, description, acceptance_criteria, attachments]:
                if len(pattern) > 0:
                    pattern = self.cleaner.check_punct(pattern)
                    patterns.append(pattern)

            text = ' '.join(patterns)
            
            backlog.append({
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

        self.backlog = pd.DataFrame(backlog)
        pd.DataFrame(self.backlog).to_csv(self.backlog_file, index=False)