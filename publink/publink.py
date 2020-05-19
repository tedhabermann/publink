"""General functions to extract and relate publications to data."""
import requests

from publink import xdd_search


def search_xdd(search_terms, account_for_spaces=True):
    """Search xDD by term.

    Parameters
    ----------
    search_terms: str
        comma separated search terms, no spaces e.g. "10.5066,10.4344"
    account for spaces: Bool
        True searchces exact match with spaces (see xdd_search.SearchXdd.all_search_terms)
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


def xdd_mentions(xdd_response, search_terms, search_type='exact_match', is_doi=False):
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
    if search_type == 'exact_match':
        mention.get_exact_mention(is_doi)
    elif search_type == 'usgs':
        mention.get_usgs_doi_mentions()

    return mention


def pair_dois(mentions):
    """Get unique list of paired DOIs.

    Get unique pairs of publication DOIs with searched terms.

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
    pairs: list of dictionaries
        [{'pub_doi': '10.3133/OFR20191040',
          'search_term': '10.5066/P9LYUFRH'
          }]

    """
    pairs = [
        {"pub_doi": i["pub_doi"],
         "search_term":i["search_term"]
         } for i in mentions
    ]

    # remove duplicate pairs
    pairs = [
        dict(t) for t in {tuple(d.items()) for d in pairs}
    ]

    return pairs


def doi_list_related(pairs):
    """Create dictionary with list of related dois.

    Puts related DOIs into format used by doi_tool module.

    Parameters
    ----------
    pairs: list of dictionaries
        unique pairs of publication DOIs with searched terms
        [{'pub_doi': '10.3133/OFR20191040',
          'search_term': '10.5066/P9LYUFRH'
          }]

    Returns
    ----------
    list_related: list of dictionaries
        list of dictionary pairs of search terms with pub dois
        example: [{'pub_dois': ['10.23706/1111111A'],
                   'search_term': '10.5066/F79021VS'}]
    """
    search_terms = [i["search_term"] for i in pairs]
    unique_terms = list(set(search_terms))

    list_related = []
    for search_term in unique_terms:
        rel = [i["pub_doi"] for i in pairs if i["search_term"] == search_term]
        new_format = {"search_term": search_term, "pub_dois": rel}
        list_related.append(new_format)
    return list_related


def resolve_doi(doi):
    """Test if DOI resolves.

    Validate that a DOI resolves.

    Parameters
    ----------
    doi: str
        example format, e.g. '10.5066/F79021VS'

    Returns
    ----------
    Bool
        True: DOI resolves, False: DOI fails to resolve

    """
    doi_url = f"https://doi.org/{doi}"
    r = requests.head(doi_url)
    if r.status_code == 302:
        return True
    else:
        return False


def validate_dois(paired_dois):
    """Validate that DOIs resolve.

    Validate that DOIs of publications and data DOIs resolve.

    """
    pub_dois = [i["pub_doi"] for i in paired_dois]
    data_dois = [i["data_doi"] for i in paired_dois]

    # reduce overall list of dois to validate
    unique_dois = list(set(pub_dois + data_dois))

    non_resolving_dois = []
    for doi in unique_dois:
        if not resolve_doi(doi):
            non_resolving_dois.append(doi)
            # removes dictionaries that contain doi not resolving
            paired_dois = [
                i
                for i in paired_dois
                if not (i["data_doi"] == doi or i["pub_doi"] == doi)
            ]
    return paired_dois, non_resolving_dois


def doi_formatting(input_doi):
    """Reformat loosely structured DOIs.

    Currently only doing simplistic removal of 2 common http prefix
    and changing case to upper.
    End DOI should be in format NN.NNNN/*, not as url

    Parameters
    ----------
    input_doi: str

    """
    input_doi = input_doi.upper()
    input_doi = input_doi.replace(" ", "")
    if str(input_doi).startswith("HTTPS://DOI.ORG/"):
        formatted_doi = input_doi[16:]  # Remove URL prefix
    elif str(input_doi).startswith("HTTP://DX.DOI.ORG/"):
        formatted_doi = input_doi[18:]
    else:
        formatted_doi = str(input_doi)
    return formatted_doi
