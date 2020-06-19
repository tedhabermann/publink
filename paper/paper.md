---
title: 'Publink: A Python package for discovering relationships between data and publications'
tags:
  - Python
  - data citation
  - eXtract Dark Data
  - xDD
  - GeoDeepDive
  - Crossref
  - Event Data
  - DataCite
  - digital object identifiers
authors:
  - name: Daniel Wieferich
    orcid: 0000-0003-1554-7992
    affiliation: "1"
  - name: Brandon Serna
    orcid: 0000-0002-5284-6230
    affiliation: "1"
  - name: Madison Langseth
    orcid: 0000-0002-4472-9106
    affiliation: "1"
  - name: Drew Ignizio
    orcid: 0000-0001-8054-5139
    affiliation: "1"
  - name: Shanon Peters
    orcid: 0000-0002-3346-4317
    affiliation: "2"
  - name: Ian Ross
    orcid: 0000-0003-1888-1689
    affiliation: "2"
affiliations:
 - name: U.S. Geological Survey
   index: 1
 - name: University of Wisconsin - Madison
   index: 2
date: 19 June 2020
bibliography: paper.bib
---

# Summary

Understanding how data are used across the scientific community provides many benefits to data authors, including building a better awareness and comprehension of 1) a dataset's scientific impact, 2) use cases to direct future versions, and 3) related efforts. Effectively tracking when and how data are used in the literature through time can be challenging.  This is in part due the to a lack of consistency in how data are referenced in scientific publications and whether or not publishers index data citations [@Green:2009;@Corti et al. 2019]. The Make Data Count initiative (https://makedatacount.org) is encouraging publishers to implement standard data citation policies, including requiring that authors cite data in their references list using digital object identifiers (DOIs) or other globally unique and persistent identifiers, and indexing these data citations with Crossref. This initiative will enhance the ability of data authors to track downstream use of their data. Many publishers are adopting these practices [@Cousijn:2018]; however, data citation indexing will likely not happen retroactively.

Publink provides methods to extract and build relationships between publications and the datasets they reference. Methods are included to support pipelines for tracking existing and new relationships through time. The package currently leverages two different sources of information: 1) the eXtract Dark Data (xDD) digital library and machine reading system (formally known as GeoDeepDive, https://geodeepdive.org/), and 2) Crossref Event Data (https://www.eventdata.crossref.org/guide/).

xDD is a digital library consisting of over 12.5 million publications that grows by some 8,000 documents daily via automated fetching mechanisms from multiple commercial and open access providers. xDD is deployed over cyberinfrastructure capable of supporting many different text and data mining applications. Publink uses the REST-full xDD application programming interface (API) to search for mentions of dataset-relevant terms, including dataset DOIs or titles, within the full-text content of the entire digital library. This unique method allows Publink to capture references to datasets that pre-date adoption of data citation principles [@Data Citation Synthesis Group:2014] and data citation indexing efforts [@Cousijn:2018]. In addition to providing flexible full-text search and retrieval of document metadata, the xDD API also surfaces snippets of text that surround the specified search terms. This contextualization allows individual mentions of target search terms within the retrieved document metadata to be assessed, through both manual and automated mechanisms.   

The metadata schema for Crossref DOIs contains an element for a list of items cited by the publication and an element for related identifiers [@Crossref:2020]. @Cousijn:2018 encourages publishers to use one of these methods to document data citations from publications. Likewise, the metadata schema for DataCite DOIs contains an element for related identifiers to link the dataset to other related resources such as citing publications and other datasets [@DataCite Metadata Working Group: 2019]. Crossref Event Data brings these documented relationships together in one location and also documents relationships between Crossref and DataCite DOIs and other content on the web, such as Twitter or Reddit mentions. Publink extracts relationships from Crossref Event Data that indicate a publication is citing a dataset of interest. 

Publink can accept three types of input to search for relationships between data citations and publications: 1) Dataset search terms, such as the dataset title, 2) Dataset DOIs, or 3) DOI prefix for an organization. Only xDD can be queried for search terms. Both xDD and Crossref Event Data can be queried for dataset DOIs and DOI prefixes. As such, publink can be useful for individual authors, project teams, and organizations to discover how their data are being used in publications. Publink also includes methods that transform and store relationships between DOIs using properties and formats consistsent with the DataCite Schema [@DataCite Metadata Working Group: 2019]. 

USGS is using publink methods to discover mentions of our own data products in scientific publications. Relationships between data and publications are tracked in the DOI metadata of our data products. This facilitates sharing of the information to our data authors and others through DataCite and Crossref Event Data.  


# References





