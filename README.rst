=======
publink
=======

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

.. image:: https://img.shields.io/badge/security-bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
   
.. image:: https://img.shields.io/travis/mlangseth/publink.svg
        :target: https://travis-ci.com/mlangseth/publink

.. image:: https://readthedocs.org/projects/publink/badge/?version=latest
        :target: https://publink.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Methods to help build relationships between data and the publications they are referenced in.

* Free software: unlicense
* Documentation: https://publink.readthedocs.io.



Contacts
-------
* Daniel Wieferich (dwieferich@usgs.gov)
* Brandon Serna (bserna@usgs.gov)
* Madison Langseth (mlangseth@usgs.gov)
* Drew Ignizio (dignizio@usgs.gov)

Purpose
-------
Understanding how data are used across the scientific community provides many benefits to data owners including building a better understand of 1) a dataset's scientific impact 2) use cases to direct future versions, 3) related efforts.  There are few efforts that help authors track how their data are being used in literature through time.  This is in part due the to a lack of consistency in how data are referenced in citations and a currently evolving field of data science allowing for the management and distribution of this information.  

This package provides methods to help extract and build relationships between publications and the datasets they reference.   Methods are developed to support pipelines to track how these relationships change through time. The package currently leverages two very different sources including the eXtract Dark Data Database (xDD, formally known as GeoDeepDive, https://geodeepdive.org/) and Crossref Event Data (https://www.eventdata.crossref.org/guide/).  The xDD digital library of over 12 million publications can be leveraged to search all mentions of search terms, including digital object identifiers.  This unique method allows us to capture relationships that dated many of the current reporting efforts, and or have not been reported to those managing this type of information.   Crossref Event Data tracks events that house relationships between registered content and something out in the web.  Currently we leverage their API to extract known references between publication DOIs and datasets of interest.  

We also include methods demonstrating how we plan to store relationships discovered with publink within the DataCite Digital Object Identifier (DOI) metadata.  Storing these relationships in the DOI metadata will allow us to pass the relationships back to Event Data and use the information in other tools such as providing citation counts on our data repository landing pages.
 
Requirements
------------
Requirements.txt shows condensed version of packages, while requirements_dev shows a full list of packages used in development.

Getting Started
---------------
Install the package

* pip install PLACEHOLDER


Example 1 queries xDD for mentions of two DOIs and returns relationships between publications and the searched DOIs.

.. code-block:: python
	
	# Import packages
	from publink import publink
	
	# Define search terms
	# Note comma separated text string with no spaces
	terms = "10.5066/P9IGEC9G,10.5066/F7K935KT"
	
	# Search xDD for DOI mentions of two DOIs
	search = publink.search_xdd(
		terms, account_for_spaces=True
		)
	 
	mention = publink.xdd_mentions(
	 	search.response_data, search.search_terms, 
	 	search_type='exact_match', is_doi=True
	 	)
	# print first two mentions
	print (mention.mentions[0:2])
	
Example 1 results of print statement to show output data structure.  Note values may differ.

.. code-block:: JSON

  [{'xdd_id': '5a0493b1cf58f1b96402aa7c',
    'pub_doi': '10.1002/2017WR020457',
    'search_term': '10.5066/F7K935KT',
    'highlight': 'DATABASE, IN U.S. GEOLOGICAL SURVEY DATA RELEASE, DOI:10.5066/F7K935KT. BELLMORE,'
	},
   {'xdd_id': '585b4a6ccf58f1a722da91ea',
    'pub_doi': '10.1002/ESP.4023',
    'search_term': '10.5066/F7K935KT',
    'highlight': 'SCIENCE DATABASE. DOI:10.5066/F7K935KT. BRANDT SA. 2000. CLASSIFICATION OF GEOMORPHOLOGICAL'
	}]

Example 2 queries xDD for mentions of two dataset title names and returns relationships between publications and the searched DOIs. Note that unlike DOI results further investigation of these results should be taken out to validate mentions.

.. code-block:: python
	
	# Import packages
	from publink import publink
	
	# Define search terms
	# Note comma separated text string with no spaces
	terms = "PAD-US,Protected Areas Database of the United States"
	
	# Search xDD for DOI mentions of two DOIs
	search = publink.search_xdd(
		terms, account_for_spaces=True
		)
	 
	mention = publink.xdd_mentions(
	 	search.response_data, search.search_terms, 
	 	search_type='exact_match', is_doi=False
	 	)
		
	# print first two mentions
	print (mention.mentions[0:2])
	
Example 2 results of print statement to show output data structure.  Note values may differ.

.. code-block:: JSON

  [{'xdd_id': '5c1c34751faed655488963fc',
    'pub_doi': '10.1016/J.FORPOL.2018.03.009',
    'search_term': 'PAD-US',
    'highlight': 'THE PROTECTED AREAS DATABASE OF THE UNITED STATES (PAD-US) (USGS, 2013). MEAN SLOPE'
	},
	{'xdd_id': '5c1cd6271faed655488975f8',
     'pub_doi': '10.1016/J.BIOCON.2018.05.019',
     'search_term': 'PAD-US',
     'highlight': 'DATABASE OF THE UNITED STATES (PAD-US, VERSION 1.4) (DELLASALA ET AL., 2001; USGS,'
	 }]
	
	
Documentation
-------------
Documentation can be found https://publink.readthedocs.io

Documentation HTML can be generated using this command from the docs folder. 

``
make html
``

Copyright and License
---------------------
This USGS product is considered to be in the U.S. public domain, and is licensed under
[unlicense](https://unlicense.org/).

This software is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely best science. The software has not received final approval by the U.S. Geological Survey (USGS). No warranty, expressed or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor shall the fact of release constitute any such warranty. The software is provided on the condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the software.




This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
