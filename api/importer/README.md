
Setup a corpus file like corpus.projectA.raw.csv that contains the user stories. The file is a CSV file exported from the user story management e.g., Jira.

--- Field Descriptions ---
Key:         Defines a unique identifier for the user story
Text:        Text is the user story itself
Attachments: Images, documents that are attached to the user story. The attachments are defined as strings and are separated by commas.
Has.*:       Are the labels that define if the user story has the respective section.
              1 means that the section is present, 0 means that the section is not present. It is used for training the support vector machine (SVM) for the Format Complete metric.
--- Field Descriptions ---