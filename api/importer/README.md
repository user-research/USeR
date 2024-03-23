
# Importer and *.csv files

For the importer, please set up a backlog file like backlog.p1.raw.csv that contains the raw user stories. The file is a CSV file that could be exported from the user story management tools e.g., Jira. Following possible fields in a demo CSV export file.

--- Field Descriptions ---
Key:                A unique technical number for the user story
Shortname:          A title or key text which identifies the user story
Description:        Typically the text "As a persona, I will ..., so ..." 
Linked.Issues:      Key of related sub-tasks and user story
Akzeptanzkriterien: Acceptance criteria
Images:             Path, filename to attached screens or user interface documents 
Attachments:        Path, filename to related documents, text files as strings and are separated by commas.
Story.Points:       Story points from an estimation
Has.*:              Are the labels that define if the user story has the respective section.
                    1 means that the section is present, 0 means that the section is not present.
                    It is used for training the support vector machine (SVM) for the Format Complete metric.
--- Field Descriptions ---