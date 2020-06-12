"""General functions to extract and relate publications to data."""
import requests

from publink import xdd_search
from publink import eventdata


def search_xdd(search_terms, account_for_spaces=True):
    """Search xDD by term.

    Parameters
    ----------
    search_terms: str
        comma separated search terms, no spaces e.g. "10.5066,10.4344"
    account for spaces: Bool
        True searches iterations of search_term with spaces inserted at each
            position to account for line or page breaks in the middle of a word
            (see xdd_search.SearchXdd.all_search_terms)
        False only searches exact match of provided search terms,

    Returns
    ----------
    search: obj
        SearchXdd object containing search results and messages

    """
    search = xdd_search.SearchXdd(search_terms)
    if account_for_spaces:
        search.all_search_terms()
    search.build_query_urls(params="full_results&clean&inclusive=True")
    search.get_data()

    return search


def xdd_mentions(xdd_response, search_terms, search_type="exact_match", is_doi=False):
    """Get mentions of search term from xDD.

    Parameters
    ----------
    xdd_response: json
        Response data from xDD
    search_terms: list str
        terms used to search xDD
    search_type: str
        - ``'exact_match'``: This default search type searches for exact
        representation of the search term(s) provided.
        - ``'usgs'``: This search type searches for usgs dois which
        have a specific format allowing for refined search.

    Returns
    ----------
    mention: obj
        xdd_search.GetMentions object containing mentions and messages

    """
    mention = xdd_search.GetMentions(xdd_response, search_terms)
    if search_type == "exact_match":
        mention.get_exact_mention(is_doi)
    elif search_type == "usgs":
        mention.get_usgs_doi_mentions()

    return mention


def search_eventdata(search_term, search_type, mailto):
    """Search eventdata by term.

    See eventdata docs @ https://www.eventdata.crossref.org/guide/

    Parameters
    ----------
    search_terms: str
        term to search, either doi prefix formatted like "10.5066"
        or doi formatted like "10.5066/P9IGEC9G"
    search_type: str, default "doi"
        - ``'doi'``: filter type that queries specific DOI.
        - ``'doi_prefix'``: filter type that queries DOI prefix
    mailto: str
        email contact, requested by crossref to help understand
        who is using their api

    Returns
    ----------
    search: obj
        SearchEventdata object containing search results and messages

    Notes
    ----------
    In dev this api fails more times than succeeds and may require
    several attempts before getting successful return

    """
    search = eventdata.SearchEventdata(search_term, search_type, mailto)
    search.build_query_url()
    search.get_data()

    return search


def eventdata_mentions(eventdata_response):
    """Get mentions of search term from xDD.

    Parameters
    ----------
    eventdata_response: json
        Response from eventdata query.  SearchEventdata response_data

    Returns
    ----------
    mention: obj
        eventdata.GetRelated object containing mentions and messages

    """
    mention = eventdata.GetRelated(eventdata_response)
    mention.get_related_dois()

    return mention


def to_related_identifiers(mentions):
    """Reformat mentions to match DataCite's schema for storing identifier relationships.

    Reformats mentions relating two DOIs to DataCite's schema that is
    used to capture related-identifiers.  This format will likely
    be needed if a user wants to write relationships back to DOIs
    through DataCite or an associated DataCite broker.
    See references:
    https://support.datacite.org/docs/relationtype_for_citation
    https://schema.datacite.org/

    Parameters
    ----------
    mentions: list of dictionaries
        For those mentions relating 2 DOIs
        example xdd_search GetMentions.mentions
            [{'xdd_id':'5d41e5e40b45c76cafa2778c',
              'pub_doi': '10.3133/OFR20191040',
              'search_term': '10.5066/P9LYUFRH',
              'highlight': 'str that ref usgs doi 10.5066/P9LYUFRH''
               }]

    Returns
    ----------
    related_identifiers: list of dictionaries
        example format shown below
        [
        {"doi":"10.5438/0012",
         "identifier":"https://doi.org/10.5438/0012",
         "related-identifiers":[
                {"relation-type-id":"Documents",
                 "related-identifier":"https://doi.org/10.5438/0013"
                 },
                {"relation-type-id":"IsNewVersionOf",
                 "related-identifier":"https://doi.org/10.5438/0010"
                 }
            ]
         }
        ]

    """
    # Get unique pairs
    unique_pairs = get_unique_pairs(mentions)

    # Get unique list of search term DOIs
    search_dois = list(set([i["search_term"] for i in unique_pairs]))

    # Get unique list of related pub dois
    pub_dois = list(set([i["pub_doi"] for i in unique_pairs]))

    # Reduce overall list of dois to test resolve
    unique_dois = list(set(pub_dois + search_dois))

    resolving_dois, non_resolving_dois = validate_dois(unique_dois)

    related_identifiers = []
    for doi in search_dois:
        # Set to DataCite Schema
        related_ids = [
            {
                "relation-type-id": "IsReferencedBy",
                "related-identifier": f"https://doi.org/{i['pub_doi']}",
            }
            for i in unique_pairs
            if i["pub_doi"] in resolving_dois and i["search_term"] in resolving_dois
        ]

        if len(related_ids) > 0:
            related = {
                "doi": doi,
                "identifier": f"https://doi.org/{doi}",
                "related-identifiers": related_ids,
            }
            related_identifiers.append(related)

    return related_identifiers


def resolve_doi(doi):
    """Test if DOI resolves.

    Validate that a DOI resolves correctly by
    giving a 302 status implies it found a
    redirect.  This is evidence that the passed
    URL is likely an active DOI.
    If a DOI does not resolve it will give a 404 status.

    Parameters
    ----------
    doi: str
        example format, e.g. '10.5066/F79021VS'

    Returns
    ----------
    Bool
        True: DOI resolves, False: DOI fails to resolve

    Note: This logic is based off initial testing.
    A better understanding of requests.head and 302
    status code should be validated. E.g. are all
    302 codes going to fully resolve if redirect is
    followed.

    """
    doi_url = f"https://doi.org/{doi}"
    r = requests.head(doi_url)
    if r.status_code == 302:
        return True
    else:
        return False


def validate_dois(doi_list):
    """Validate that each DOI in list resolves.

    Parameters
    ----------
    doi_list: list of strings
        list of DOIs
        example format ['10.5066/F79021VS']

    Returns
    ----------
    resolving_dois: list of strings
        DOIs that did resolve
    non_resolving_dois: list of strings
        DOIs that did not resolve

    """
    # Ensure we are validating each DOI only once
    unique_dois = list(set(doi_list))

    non_resolving_dois = []
    resolving_dois = []
    for doi in unique_dois:
        if resolve_doi(doi):
            resolving_dois.append(doi)
        else:
            non_resolving_dois.append(doi)
    return resolving_dois, non_resolving_dois


def get_unique_pairs(mentions):
    """Get unique pairs of search term and pub DOI.

    Parameters
    ----------
    mentions: list of dictionaries
        example xdd_search GetMentions.mentions
            [{'xdd_id':'5d41e5e40b45c76cafa2778c',
              'pub_doi': '10.3133/OFR20191040',
              'search_term': '10.5066/P9LYUFRH',
              'highlight': 'str that ref usgs doi 10.5066/P9LYUFRH''
               }]

    Returns
    ----------
    unique_pairs: dictionary
        unique sets of publication, search term pairs
        example format below
        [{'pub_doi': '10.3133/OFR20191040',
          'search_term': '10.5066/P9LYUFRH'
          }]

    """
    pairs = [
        {"pub_doi": i["pub_doi"], "search_term": i["search_term"]} for i in mentions
    ]

    # remove duplicate pairs
    unique_pairs = [dict(t) for t in {tuple(d.items()) for d in pairs}]

    return unique_pairs


def doi_formatting(input_doi):
    """Reformat loosely structured DOIs.

    Currently only doing simplistic removal of 8 common http prefixes
    and changing case to upper.
    End DOI should be in format 10.NNNN/*, not as url

    Parameters
    ----------
    input_doi: str

    Notes
    ----------
    This focuses on known potential issues.  This currently
    returns no errors, potential improvement for updates.

    """
    input_doi = input_doi.upper()
    input_doi = input_doi.replace(" ", "")
    # All DOI prefixes begin with '10'
    if str(input_doi).startswith("10"):
        formatted_doi = str(input_doi)
    elif str(input_doi).startswith("DOI:"):
        formatted_doi = input_doi[4:]
    elif str(input_doi).startswith("HTTPS://DOI.ORG/DOI:"):
        formatted_doi = input_doi[20:]
    elif str(input_doi).startswith("HTTPS://DX.DOI.ORG/DOI:"):
        formatted_doi = input_doi[23:]
    elif str(input_doi).startswith("HTTP://DOI.ORG/DOI:"):
        formatted_doi = input_doi[19:]
    elif str(input_doi).startswith("HTTP://DX.DOI.ORG/DOI:"):
        formatted_doi = input_doi[22:]
    elif str(input_doi).startswith("HTTPS://DOI.ORG/"):
        formatted_doi = input_doi[16:]
    elif str(input_doi).startswith("HTTPS://DX.DOI.ORG/"):
        formatted_doi = input_doi[19:]
    elif str(input_doi).startswith("HTTP://DOI.ORG/"):
        formatted_doi = input_doi[15:]
    elif str(input_doi).startswith("HTTP://DX.DOI.ORG/"):
        formatted_doi = input_doi[18:]
    else:
        formatted_doi = str(input_doi)
    return formatted_doi
