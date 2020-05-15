"""Main module."""
import requests

from publink import xdd_search


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


def doi_list_related(paired_dois):
    """Create dictionary with list of related dois.

    Puts related DOIs into format used by doi_tool module.

    Parameters
    ----------
    paired_dois: list of dictionaries
        list of dictionary pairs of data dois with pub dois
        example: [{'pub_doi': '10.23706/1111111A',
        'data_doi': '10.5066/F79021VS'}]

    Returns
    ----------
    doi_list_related: list of dictionaries
        list of dictionary pairs of data dois with pub dois
        example: [{'pub_dois': ['10.23706/1111111A'],
        'data_doi': '10.5066/F79021VS'}]
    """
    data_dois = [i["data_doi"] for i in paired_dois]
    unique_dois = list(set(data_dois))

    doi_list_related = []
    for data_doi in unique_dois:
        rel = [i["pub_doi"] for i in paired_dois if i["data_doi"] == data_doi]
        new_format = {"data_doi": data_doi, "pub_dois": rel}
        doi_list_related.append(new_format)
    return doi_list_related


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
    if str(input_doi).startswith("HTTPS://DOI.ORG/"):
        formatted_doi = input_doi[16:]  # Remove URL prefix
    elif str(input_doi).startswith("HTTP://DX.DOI.ORG/"):
        formatted_doi = input_doi[18:]
    else:
        formatted_doi = str(input_doi)
    return formatted_doi


def xdd_usgs_referenced_dois(search_terms):
    """Import paired DOIs from xDD searches.

    Parameters
    ----------
    search_terms: list
        list of strings to search

    Returns
    ----------
    paired_dois: list of dictionaries
        list of dictionary pairs of data dois with pub dois
        example: [{'pub_doi': '10.23706/1111111A',
        'data_doi': '10.5066/F79021VS'}]

    """
    paired_dois = []
    for search_term in search_terms:
        data = xdd_search.SearchXdd(search_term)
        data.build_query(params="full_results&clean&inclusive=True")
        data.query_xdd()
        data.get_doi_mentions()
        paired_dois.extend(data.related_dois)
    # Remove duplicate dictionaries from list
    paired_dois = [dict(t) for t in {tuple(d.items()) for d in paired_dois}]

    return paired_dois


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
