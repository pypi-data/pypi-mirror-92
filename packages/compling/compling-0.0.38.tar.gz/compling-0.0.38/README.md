# compling
#### Computational Linguistic with Python

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

**compling** is a Python module that provides some **_Natural Language Processing_** and **_Computational Linguistics_** functionalities to work with human language data. It incorporates various _Data_ and _Text Mining_ features from other famous libraries (e.g. [spacy](https://pypi.org/project/spacy/), [nltk](https://pypi.org/project/nltk/), [sklearn](https://pypi.org/project/scikit-learn/), ...) in order to arrange a pipeline aimed at the analysis of corpora of _JSON_ documents.

### Documentation
 See documentation [here](http://pycompling.altervista.org/).

### Installation
You can install **compling** with:
```sh
$ pip install compling
```
**compling** requires:
+ _Python_ (>= 3.6)
+ _numpy_
+ _spacy_
+ _nltk_
+ _gensim_
+ _tqdm_
+ _unicodedata2_
+ _unidecode_
+ configparser_
+ _vaderSentiment_
+ _wordcloud_

You also need to download:
* a ++_spacy language model_++ <br/>
See [here](https://spacy.io/models) the available models. You can choose based on the language of your corpus documents. 
By default, **complig** expects you to download _sm_ models. You can still choose to download larger models, but remember to edit the [_confg.ini_](#config.ini) file, so it can work properly.

    _Example_ <br/>
    Let's assume the language of your documents is _English_. 
    You could download the _spacy small english model_:
    ```sh
    python -m spacy download en_core_web_sm
    ```
* some ++_nltk functionalities_++: <br/>
    * _stopwords_
        ```sh
        $ python -m nltk.downloader stopwords
        ```
    * _punkt_
        ```sh
        $ python -m nltk.downloader punkt
        ```
### config.ini
The functionalities offered by **compling** may require a large variety of parameters. To facilitate their use, default values are provided for some parameters:
- some can be changed in the function invocation. Many functions provide optional parameters;
- others are stored in the ++_config.ini_++ file.
  This file configures the processing of your corpora. It contains the values of some special parameters. 
  (e.g. _the language of documents in your corpus._)

You can see a preview below:
```ini
[Corpus]
;The language of documents in your corpus.
language = english

;Documents in your corpus store their text in this key.
text_key = text

;Documents in your corpus store their date values as string in this format.
;For a complete list of formatting directives, see: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior.
date_format = %d/%m/%Y

;The size of spacy model you want it to be used in the text processing
spacy_model_size = md

[Document_record]
;Document records metadata:

;If lower==1, A lowercase version will be stored for each document.
lower = 0

;If lemma==1, A version with tokens replace by their lemma will be stored for each document.
lemma = 0

;If stem==1, A version with tokens replace by their stem will be stored for each document.
stem = 0

;If negations==1, A version where negated token are preceded by 'NOT_' prefix will be stored for each document.
negations = 1

;If named_entities==1, the occurring named entities will be stored in a list for each document.
named_entities = 1
; ...
```
##### ConfigManager
**compling** provides the _ConfigManager_ class to make it easier for you to edit the _config.ini_ file and to help you handling the corpora processing .

#### example of usage (compling)
You can see a short example of usage at [https://github.com/FrancescoPeriti/compling](https://github.com/FrancescoPeriti/compling). 

See the [documentation](http://pycompling.altervista.org/) for more details.