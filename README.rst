=======
publink
=======

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

.. image:: https://readthedocs.org/projects/publink/badge/?version=latest
        :target: https://publink.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://codecov.io/gh/usgs-biolab/publink/branch/main/graph/badge.svg
  :target: https://codecov.io/gh/usgs-biolab/publink

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

.. image:: https://github.com/usgs-biolab/publink/workflows/Python%20package/badge.svg
    :target: https://github.com/usgs-biolab/publink/actions?query=workflow%3A%22Python+package%22t
    :alt: Github Actions

.. image:: https://img.shields.io/badge/security-bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status

Python package with methods to help build relationships between data and the publications they are referenced in.

* Free software: unlicense
* Documentation: https://publink.readthedocs.io.


.. image:: logo.JPG
    :width: 50 %

Contacts
--------
* Daniel Wieferich (dwieferich@usgs.gov)
* Brandon Serna (bserna@usgs.gov)
* Madison Langseth (mlangseth@usgs.gov)
* Drew Ignizio (dignizio@usgs.gov)

Purpose
-------
Understanding how data are used across the scientific community provides many benefits to data authors, including building a better awareness and comprehension of 1) a dataset's scientific impact, 2) use cases to direct future versions, and 3) related efforts. Effectively tracking when and how data are used in the literature through time can be challenging.  This is in part due to a lack of consistency in how data are referenced in scientific publications and whether or not publishers index data citations [@Green:2009;@Corti et al. 2019]. The Make Data Count initiative (https://makedatacount.org) is encouraging publishers to implement standard data citation policies, including requiring that authors cite data in their references list using digital object identifiers (DOIs) or other globally unique and persistent identifiers, and indexing these data citations with Crossref. This initiative will enhance the ability of data authors to track downstream use of their data. Many publishers are adopting these practices [@Cousijn:2018]; however, data citation indexing may not happen retroactively.

Publink provides methods to extract and build relationships between publications and the datasets they reference. Methods are included to support pipelines for tracking existing and new relationships through time. The package currently leverages two different sources of information: 1) the eXtract Dark Data (xDD) digital library and machine reading system (formally known as GeoDeepDive, https://geodeepdive.org/), and 2) Crossref/DataCite Event Data (https://www.eventdata.crossref.org/guide/).

xDD is a digital library consisting of over 12.5 million publications that grows by some 8,000 documents daily via automated fetching mechanisms from multiple commercial and open access providers. xDD is deployed over cyberinfrastructure capable of supporting many different text and data mining applications. Publink uses the REST-full xDD application programming interface (API) to search for mentions of dataset-relevant terms, including dataset DOIs or titles, within the full-text content of the entire digital library. This unique method allows Publink to capture references to datasets that pre-date adoption of data citation principles [@Data Citation Synthesis Group:2014] and data citation indexing efforts [@Cousijn:2018]. In addition to providing flexible full-text search and retrieval of document metadata, the xDD API also surfaces snippets of text that surround the specified search terms. This contextualization allows individual mentions of target search terms within the retrieved document metadata to be assessed, through both manual and automated mechanisms.   

The metadata schema for Crossref DOIs contains an element for a list of items cited by the publication and an element for related identifiers [@Crossref:2020]. @Cousijn:2018 encourages publishers to use one of these methods to document data citations from publications. Likewise, the metadata schema for DataCite DOIs contains an element for related identifiers to link the dataset to other related resources such as citing publications and other datasets [@DataCite Metadata Working Group: 2019]. Crossref/DataCite Event Data brings these documented relationships together in one location and also documents relationships between Crossref and DataCite DOIs and other content on the web, such as Twitter or Reddit mentions. Publink extracts relationships from Crossref/DataCite Event Data that indicate a publication is citing a dataset of interest. 

Publink can accept three types of input to search for relationships between data citations and publications: 1) Dataset search terms, such as the dataset title, 2) Dataset DOIs, or 3) DOI prefix for an organization. Only xDD can be queried for search terms. Both xDD and Crossref/DataCite Event Data can be queried for dataset DOIs and DOI prefixes. As such, publink can be useful for individual authors, project teams, and organizations to discover how their data are being used in publications.  Publink could also assist those collecting data citation metrics. Publink also includes methods that transform and store relationships between DOIs using properties and formats consistsent with the DataCite Schema [@DataCite Metadata Working Group: 2019]. 

USGS is using publink methods to discover mentions of our own data products in scientific publications. Relationships between data and publications are tracked in the DataCite DOI metadata of our data products, which is then shared with Event Data and made available to CrossRef, and the consumers of Event Data's services. This facilitates sharing of the information to our data authors and others through Crossref/DataCite Event Data. 

Requirements
------------
Requirements.txt shows condensed version of packages, while requirements_dev shows a full list of packages used in development.

Getting Started
---------------
Install the package

* pip install git+https://github.com/usgs-biolab/publink.git


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

.. code-block::

  [{'xdd_id': '5a0493b1cf58f1b96402aa7c',
    'pub_doi': '10.1002/2017WR020457',
    'pub_title': 'Dam removal: Listening in',
	'pub_date': '2017 07',
	'pub_journal': 'Water Resources Research',
    'search_term': '10.5066/F7K935KT',
    'highlight': 'DATABASE, IN U.S. GEOLOGICAL SURVEY DATA RELEASE, DOI:10.5066/F7K935KT. BELLMORE,'
	},
   {'xdd_id': '585b4a6ccf58f1a722da91ea',
    'pub_doi': '10.1002/ESP.4023',
	'pub_title': 'Geomorphic monitoring and response to two dam removals: rivers Urumea and Leitzaran (Basque Country, Spain)',
	'pub_date': '2016',
	'pub_journal': 'Earth Surface Processes and Landforms',
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

.. code-block:: 

  [{'doi': '10.5066/F7K935KT',
    'identifier': 'https://doi.org/10.5066/F7K935KT',
    'related-identifiers': [{'relation-type-id': 'IsCitedBy',
    'related-identifier': 'https://doi.org/10.1002/WAT2.1164'},
   {'relation-type-id': 'IsCitedBy',
    'related-identifier': 'https://doi.org/10.3133/OFR20161132'},
   {'relation-type-id': 'IsCitedBy',
    'related-identifier': 'https://doi.org/10.1080/24694452.2018.1507814'},
   {'relation-type-id': 'IsCitedBy',
    'related-identifier': 'https://doi.org/10.1002/2017WR020457'},
   {'relation-type-id': 'IsCitedBy',
    'related-identifier': 'https://doi.org/10.1111/1752-1688.12450'},
   {'relation-type-id': 'IsCitedBy',
    'related-identifier': 'https://doi.org/10.3133/OFR20161165'},
   {'relation-type-id': 'IsCitedBy',
    'related-identifier': 'https://doi.org/10.1016/J.GEOMORPH.2015.07.027'},
   {'relation-type-id': 'IsCitedBy',
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

.. code-block::

  [{'xdd_id': '5c1c34751faed655488963fc',
    'pub_doi': '10.1016/J.FORPOL.2018.03.009',
    'pub_title': 'Impact of market conditions on the effectiveness of payments for forest-based carbon sequestration',
	'pub_date': 'July 2018',
	'pub_journal': 'Forest Policy and Economics',
    'search_term': 'PAD-US',
    'highlight': 'THE PROTECTED AREAS DATABASE OF THE UNITED STATES (PAD-US) (USGS, 2013). MEAN SLOPE'
	},
	{'xdd_id': '5c1cd6271faed655488975f8',
     'pub_doi': '10.1016/J.BIOCON.2018.05.019',
     'pub_title': 'Assessing threats of non-native species to native freshwater biodiversity: Conservation priorities for the United States',
	 'pub_date': 'August 2018',
	 'pub_journal': 'Biological Conservation',
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

.. code-block::

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

.. code-block::

  Successful response.
  
  [{'event_id': 'cfc4f434-60c3-407f-bd06-2c7f122867f3',
    'pub_doi': '10.1007/s10661-017-6060-x',
    'search_term': '10.5066/F7K935KT',
    'source': 'crossref
	}]


References
---------------------
Corti, L., V. Van den Eynden, B. Libby, and M. Wollard.  Oct 2019. Managing and Sharing Research Data A Guide to Good Practice Second Edition. London, Sage Publications Ltd.

Cousijn, Helena, Amye Kenall, Emma Ganley, Melissa Harrison, David Kernohan, Thomas Lemberger, Fiona Murphy, Patrick Polischuk, Simone Taylor, Maryann Martone, and Tim Clark. 2018. A data citation roadmap for scientific publishers. Sci Data 5, 180259. https://doi.org/10.1038/sdata.2018.259.

Crossref. 2020. "Deposit Schema 4.4.2." Accessed June 19, 2020. https://data.crossref.org/reports/help/schema_doc/4.4.2/index.html.

Data Citation Synthesis Group. 2014. Joint Declaration of Data Citation Principles. Martone M. (ed.) San Diego CA: FORCE11. https://doi.org/10.25490/a97f-egyk.

DataCite Metadata Working Group. 2019. DataCite Metadata Schema Documentation for the Publication and Citation of Research Data. Version 4.3. DataCite e.V. https://doi.org/10.14454/7xq3-zf69.

Green, Toby. We need publishing standards for datasets and data tables. Learned Publishing. Oct 2009. https://doi.org/10.1087/20090411.


Documentation
-------------
Documentation can be found https://publink.readthedocs.io

Documentation HTML can be generated using this command from the docs folder. 

.. code-block::

	make docs


Copyright and License
---------------------
This USGS product is considered to be in the U.S. public domain, and is licensed under unlicense_

.. _unlicense: https://unlicense.org/

This software is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely best science. The software has not received final approval by the U.S. Geological Survey (USGS). No warranty, expressed or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor shall the fact of release constitute any such warranty. The software is provided on the condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the software.




This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
