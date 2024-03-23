# Version history
* 0.1 (Mar 12, 2021)
- SVM is used to predict formal quality
- Build glossary by tfidf, named and lemma identification
- Add regression prediction for saturation quality

* 0.2 (Nov 27, 2021)
- Start multiple project handling
- Use make to cover operation tasks

* 0.3 (Dec 3, 2021)
- Optimize lexical q. (fi) to range between zero and hundred
- Optimize saturation q. (fi) to be greater or equal to zero

* 0.4 (Jan 29, 2023)

- Include backlog importer functionality with individual spaCy sentence recognizer
- Change to SVM training with greater backlog
- Add log functionality
- Include remote debugger in docker container

* 0.5 (Aug 6, 2023)

- Connect health project backlog into prediction handling
- Change indicator name "Valuable" to "Customer Speak" and "Pattern Complete" to "Format complete"
- Include training models on meta level for multi projects
- Add multiple regression evaluation
- Add "Word Sparse", "Sentence Sparse", and "Easy Language"

* 0.6 (Sep 10, 2023)

- Change API to organize metrics based on Registry Pattern
- Split APP into Python backend and React frontend applications