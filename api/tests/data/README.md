Set up a backlog TEST file like p2_backlog.csv that contains the test user stories. This file is used for the test cases in test_user.py. File can be created from a ../importer/p2_backlog_raw.csv with the CLI call > make import env=TEST.

The field descriptions must be following the format in p1_backlog.csv as they are mandatory fields for the e.g., Format Complete metric (SVM training) see ./api/importer/base_importer.py: Importer.import_backlog().

--- Field Descriptions ---
usid:    Defines a unique identifier for the user story
text:    The text of the user story
*_label: The labels define if the user story has the respective section.
         One means that the section is present, and zero indicates that the section is not present.
         It is used to train the Format Complete metric's support vector machine (SVM).
--- Field Descriptions ---