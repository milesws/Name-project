# Name-project
Description of files in repository:

Data+cleaning.ipynb
  Cleans and organizes true name matches to be vectorized
Prepare features.ipynb
  Creates the features and vectorizes the names
api_scrape.py
  Takes FamilySearch ids and retrieves the individual and the sources attached
cleaning_false_names.py
  Cleans and organizes false name matches to be vectorized
jaro_winkler.py
  Cuts out false name matches that have a jaro-winkler score of 1 or under .6
