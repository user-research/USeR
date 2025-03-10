
# Importer and *.csv files

Please set up a backlog file like p2_backlog_raw.csv for the importer that contains the raw user stories.

Below are the field descriptions from the "demo" German data set as orientation. But any other field definitions are possible. The final mapping between the provided and mandatory fields for USeR will be defined in, e.g., p2_importer.py.

--- Demo Data Set Field Descriptions ---
key:                 A unique technical number for the user story.
title:               A title or key text that identifies the user story.
description:         Typically, the text is "As a persona, I will ..., so ...". 
acceptance_criteria: Acceptance criteria.
attachments:         Paths and filenames, as strings, to related documents separated by commas.
has_*:               These labels indicate whether the user story has the respective section.
                     One means the section is present, and zero indicates it is not. This information
                     is used to train the Format Complete metric's support vector machine (SVM).
--- Demo Data Set Field Descriptions ---