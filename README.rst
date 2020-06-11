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
--------
* Daniel Wieferich (dwieferich@usgs.gov)
* Brandon Serna (bserna@usgs.gov)
* Madison Langseth (mlangseth@usgs.gov)
* Drew Ignizio (dignizio@usgs.gov)

Purpose
-------
Understanding how data are used across the scientific community provides many benefits to data authors including building a better awareness of 1) a dataset's scientific impact, 2) use cases to direct future versions, and 3) related efforts.  There are few efforts that help authors track how their data are being used in literature through time.  This is in part due to a lack of consistency in how data are referenced in scientific publications and whether or not publishers index data citations. The Make Data Count initiative (https://makedatacount.org) is encouraging publishers to implement policies that require that authors cite data in their references list and to index these data citations with Crossref. This initiative will enhance the ability of data authors to track downstream use of their data; however, many publishers have not yet adopted these practices and data citation indexing will likely not happen retroactively.

This package provides methods to help extract and build relationships between publications and the datasets they reference.   Methods have been developed that support pipelines for tracking existing and new relationships through time. The package currently leverages two different sources including the eXtract Dark Data Database (xDD, formally known as GeoDeepDive, https://geodeepdive.org/) and Crossref and DataCite Event Data (https://www.eventdata.crossref.org/guide/).  The xDD digital library of over 12 million publications can be leveraged to search all mentions of search terms, including digital object identifiers (DOIs).  This unique method allows us to capture relationships that pre-dated adoption of data citation principles (Data Citation Synthesis Group, 2014) and data citation indexing efforts.  Crossref and DataCite Event Data documents relationships between Crossref and DataCite DOIs and other content on the web.  Currently, we leverage their API to extract known references between publication DOIs and datasets of interest.  

We also include methods demonstrating how you can store relationships discovered with publink within the DataCite DOI metadata.  Storing these relationships in the DOI metadata allows relationships discovered through xDD to be included in Event Data. It also allows the use of this information in other tools such as downstream data repositories.
 
Requirements
------------
Requirements.txt shows condensed version of packages, while requirements_dev shows a full list of packages used in development.

Getting Started
---------------
Install the package

* pip install git+ssh://git@code.usgs.gov/sas/sdm/publink


**Example 1a** queries xDD for mentions of two DOIs and returns relationships between publications and the searched DOIs.
Note that search and mention variables are objects that contain data and information that can be used for reporting (e.g. logs) and Quality Assurance/Quality Control (QAQC).

.. code-block:: python
	
	# Import packages
	from publink import publink
	
	# Define search terms
	# Note comma separated text string with no spaces
	terms = "10.5066/P9IGEC9G,10.5066/F7K935KT"
	
	# Search publications in xDD for mentions of the two DOIs
	search = publink.search_xdd(
		terms, account_for_spaces=True
		)

	# Simplify and restructure output data 
	mention = publink.xdd_mentions(
	 	search.response_data, search.search_terms, 
	 	search_type='exact_match', is_doi=True
	 	)
	# print first two mentions
	print (mention.mentions[0:2])
	
**Example 1a results** of print statement to show output data structure.  Note values may differ as xDD is updated.

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
	
**Example 1b** restructures mentions from example 1a to match DataCite's schema for storing identifier relationships.

.. code-block:: python
	
	# Import packages
	from publink import publink
	
	related_identifiers = publink.to_related_identifiers(mention.mentions)
	
	print (related_identifiers)
	
**Example 1b results** of print statement to show output data structure.  Note values may differ as xDD is updated.

.. code-block:: JSON

  [{'doi': '10.5066/F7K935KT',
  'identifier': 'https://doi.org/10.5066/F7K935KT',
  'related-identifiers': [{'relation-type-id': 'IsReferencedBy',
    'related-identifier': 'https://doi.org/10.1002/WAT2.1164'},
   {'relation-type-id': 'IsReferencedBy',
    'related-identifier': 'https://doi.org/10.3133/OFR20161132'},
   {'relation-type-id': 'IsReferencedBy',
    'related-identifier': 'https://doi.org/10.1080/24694452.2018.1507814'},
   {'relation-type-id': 'IsReferencedBy',
    'related-identifier': 'https://doi.org/10.1002/2017WR020457'},
   {'relation-type-id': 'IsReferencedBy',
    'related-identifier': 'https://doi.org/10.1111/1752-1688.12450'},
   {'relation-type-id': 'IsReferencedBy',
    'related-identifier': 'https://doi.org/10.3133/OFR20161165'},
   {'relation-type-id': 'IsReferencedBy',
    'related-identifier': 'https://doi.org/10.1016/J.GEOMORPH.2015.07.027'},
   {'relation-type-id': 'IsReferencedBy',
    'related-identifier': 'https://doi.org/10.1002/ESP.4023'}]
	}]

**Example 2** queries xDD for mentions of two dataset title names and returns relationships between publications and the searched DOIs. Note that, unlike DOI results, further investigation of these results should be considered to validate mentions. This method is ideal for datasets without assigned DOIs or for datasets with DOIs that were assigned after initial dataset publication.

.. code-block:: python
	
	# Import packages
	from publink import publink
	
	# Define search terms
	# Note comma separated text string with no spaces
	terms = "PAD-US,Protected Areas Database of the United States"
	
	# Search publications in xDD for mentions of the two titles
	search = publink.search_xdd(
		terms, account_for_spaces=True
		)
	
	# Simplify and restructure output data  
	mention = publink.xdd_mentions(
	 	search.response_data, search.search_terms, 
	 	search_type='exact_match', is_doi=False
	 	)
		
	# print first two mentions
	print (mention.mentions[0:2])
	
**Example 2 results** of print statement to show output data structure.  Note values may differ as xDD is updated. Additionally, note that PAD-US version 1.4 was assigned a DOI; however, the publication found in xDD did not reference the DOI.

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

**Example 3** queries xDD for mentions of all USGS DOIs with the prefix "10.5066" and returns relationships between publications and the USGS data DOIs. This technique requires prior knowledge of DOI format and currently uses methods specific to USGS (e.g. all USGS DOIs are 16 characters long). 

.. code-block:: python
	
	# Import packages
	from publink import publink
	
	# Search publications in xDD for mentions of all USGS DOIs with prefix "10.5066"
	search = publink.search_xdd(
		"10.5066", account_for_spaces=True
		)
	 
	mention = publink.xdd_mentions(
	 	search.response_data, search.search_terms, 
	 	search_type='usgs', is_doi=True
	 	)
		
	# print first two mentions
	print (mention.mentions[0:2])
	
**Example 3 results** of print statement to show output data structure.  Note values may differ as xDD is updated.

.. code-block:: JSON

  [{'xdd_id': '5e62d6d1998e17af82642c1c',
    'pub_doi': '10.3133/SIM3428',
    'search_term': '10.5066/P91HL91C',
	'certainty': 'most certain',
    'highlight': 'ARABIA: U.S. GEOLOGICAL SURVEY DATA RELEASE, DOI:10.5066/P91HL91C. DOWNS, D.T., STELTEN, M.E., CHAMPION,'
	},
   {'xdd_id': '5e62de89998e17af82642dec',
    'pub_doi': '10.3133/SIR20195140',
    'search_term': '10.5066/F7P55KJN',
	'certainty': 'most certain',
    'highlight': 'DATABASE, ACCESSED JUNE 10, 2018, AT HTTPS://DOI. ORG/10.5066/F7P55KJN. WHEELER, J.D., AND EDDY-MILLER,'
	}]

**Example 4** queries eventdata for events that mention a DOI being referenced by another DOI (publication DOI).  We note that calls to the eventdata API were unstable at the time of development. If no data are returned, verify the success of the query.  Prefix searches can be conducted with search_type="doi_prefix".  

.. code-block:: python

	# Import packages
	from publink import publink
	
	# DOI to search, note the format
	search_term = "10.5066/F7K935KT"

	# Search eventdata for DOI events
	search = publink.search_eventdata(
		search_term, search_type="doi",
		mailto='dwieferich@usgs.gov'
		)

	# Print search message
	print (search.response_message + '\n')

	# Get Events that mention DOI being referenced by another DOI (pub_doi)
	mention = publink.eventdata_mentions(
		search.response_data
		)

	# Print first two mentions
	print (mention.related_dois[0:2])
	
**Example 4 results** of print statements to show output data structure.  Note values may differ as eventdata is updated.

.. code-block:: JSON

  Successful response.
  
  [{'event_id': 'cfc4f434-60c3-407f-bd06-2c7f122867f3',
    'pub_doi': '10.1007/s10661-017-6060-x',
    'search_term': '10.5066/F7K935KT',
    'source': 'crossref
	}]


References
---------------------
Data Citation Synthesis Group, 2014, Joint Declaration of Data Citation Principles, Martone M. (ed.): FORCE11, https://doi.org/10.25490/a97f-egyk.


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
