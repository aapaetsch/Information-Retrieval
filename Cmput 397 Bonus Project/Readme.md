- nltk documentation consulted found at http://www.nltk.org/
- tokenization function from assignment 2 modified and implemented, original version can be found in our assignment 2 repository at https://github.com/UAlberta-CMPUT397-W19/cmput397-w19-proj2-dhoeppne
<br /><br />
<h2>Assumptions: </h2>

- Boolean queries are supported by this index, however there is no way to input them into the queries for lm_query.py. 
- Directories used in the command line arguments are relational, so for instance if you are in the directory where ```create_index.py``` is 
but the movies folder is one level up, the directory entered should be ../cmput397_2k_movies instead of just cmput397_2k_movies
- The above is also true for entering directories into lm_query
- I assume that we do not need to do phrase queries since I used a unigram model 
- Tokenization uses stemming, however does not remove stop words as this is a language model and removing them resulted in many empty queries
- At the begining of each program an alert about downloading nltk will print, I do not get rid of this as using cls or clear would clear the entire terminal output

<h2>Instructions to run</h2>

1. To install nltk, run ```pip3 install nltk```
2. If any other libraries under the libraries used section are missing, they can be installed with ```pip3 install <library name>```
2. To run ```create_index.py```, use ```python3 create_index.py <Directory to be Indexed> <Output Directory>```
3. ```create_index.py``` must be run before ```lm_query.py``` as the index is needed before queries can be run.
4. To run queries, you must use ```python3 lm_query.py <Directory of Index> <K> <y/n> <keywords>...```
5. Keywords must be separated by spaces, K must be an integer, <y/n> will take y or yes with any mix of uppercase however n will be defaulted to if anything else is entered

<h2>Libraries used<h2>

- json
- nltk
- math
- string
- os
- sys
