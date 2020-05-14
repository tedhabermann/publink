"""Extract info from eXtract Dark Data (xDD) (https://geodeepdive.org/)."""

# Import packages
import requests
import bs4
import re
from publink import publink


class SearchXdd():
    """Class allowing for searching of xDD publication database."""

    def __init__(self, search_term="10.5066", route="snippets"):
        """Initialize search pubs object.

        Parameters
        ----------
        search_term: str, default is USGS DOI prefix "10.5066"
            term to search across xDD corpus
        route: str, default "snippets"
            available routes described at https://geodeepdive.org/api

        Notes
        ----------
        Search terms not available for all routes in xDD

        """
        self.xdd_api_base = "https://geodeepdive.org/api"
        self.search_term = search_term
        self.route = route
        self.response_data = []
        self.search_url = None
        self.next_url = ""
        self.response_status = "error"
        self.response_message = "No request made."

    def build_query(self, params="full_results&clean"):
        """Build xDD query to search user defined string."""
        api_route = f"{self.xdd_api_base}/{self.route}"
        q = f"?term={self.search_term}&{params}"
        self.search_url = f"{api_route}{q}"
        self.next_url = self.search_url

    def query_xdd(self):
        """Query xDD for results."""
        while self.next_url != "":
            r = requests.get(self.next_url)
            if r.status_code == 200 and "success" in r.json():
                json_response = r.json()
                self.response_hits = json_response["success"]["hits"]
                page_data = json_response["success"]["data"]
                self.response_data.extend(page_data)
                self.next_url = json_response["success"]["next_page"]
            else:
                self.next_url = ""
                if r.status_code == 200 and "success" not in r.json():
                    self.response_status = "no data"
                    self.response_message = f"Request returned no data. \
                        Verify request is valid."
                elif r.status_code != 200:
                    self.response_status = "error"
                    self.response_message = f"Request returned status code: \
                        {r.status_code}."
                else:
                    self.response_status = "error"
                    self.response_message = f"Unknown error."
            self.response_status = "success"
            self.response_message = "Successful response."

    def get_doi_mentions(self):
        """Get mentions of DOIs from xDD snippets.

        Returns
        ----------
        self.related_dois: list of dictionaries
            list of dictionary pairs of data dois with pub dois
            example: [{'pub_doi': '10.23706/1111111A',
            'data_doi': '10.5066/F79021VS'}]
        self.missing_pub_doi: list
            list of data dois that xDD does not have a DOI for
            the associated publication.  These DOI mentions may
            still be important to a user but no relationship will
            be documented in the DOI Tool.
        """
        self.missing_pub_doi = []
        self.related_dois = []
        for ref in self.response_data:
            if "doi" in ref.keys() and ref["doi"] != "":
                ref_doi = publink.doi_formatting(ref["doi"])
                doi_mentions_for_ref = []
                for i_link in ref["highlight"]:
                    doi_mentions = extract_doi(self.search_term, i_link)
                    if len(doi_mentions) > 0:
                        doi_mentions_for_ref.extend(doi_mentions)
                doi_mentions_for_ref = list(set(doi_mentions_for_ref))
                new = [{"pub_doi": ref_doi, "data_doi": mention}
                       for mention in doi_mentions_for_ref]
                self.related_dois = self.related_dois + new
            else:
                self.missing_pub_doi.append(ref)

    # def validate_dois(self):
    #     """Validate that DOIs resolve.

    #     Validate that DOIs of publications and data DOIs resolve.

    #     """
    #     pub_dois = [i['pub_doi'] for i in self.related_dois]
    #     data_dois = [i['data_doi'] for i in self.related_dois]

    #     unique_dois = list(set(pub_dois + data_dois))

    #     self.non_resolving_dois = []
    #     for doi in unique_dois:
    #         if not publink.resolve_doi(doi):
    #             self.non_resolving_dois.append(doi)
    #             self.related_dois = [
    #                 i for i in self.related_dois if not (
    #                     i['data_doi'] == doi or i['pub_doi'] == doi)
    #                 ]

    # def list_related_dois(self):
    #     """Create dictionary with list of related dois.

    #     Puts related DOIs into format used by doi_tool module.

    #     """
    #     data_dois = [i['data_doi'] for i in self.related_dois]
    #     unique_dois = list(set(data_dois))

    #     self.doi_all_related = []
    #     for data_doi in unique_dois:
    #         rel = [
    #             i["pub_doi"] for i in self.related_dois if i[
    #                 "data_doi"] == data_doi
    #                 ]
    #         new_format = {"data_doi": data_doi,
    #                       "pub_dois": rel}
    #         self.doi_all_related.append(new_format)


def extract_doi(find_str, full_txt):
    """Extract DOI that was mentioned from xDD snippet.

    Parameters
    ----------
    find_str: str
        intended to be doi prefix (example '10.5066'), but could be expanded
    full_txt: str
        text that contains the find_str

    Returns
    ----------
    doi_mention: str
        text representation of full doi (e.g. '10.5066/F79021VS')

    Notes
    ----------
    This method currently only works for highly structured USGS DOIs

    """
    # Verify DOI is not a number. These combonations
    # shouldn't occur as DOI but should be further investigated

    full_txt = clean_unicode(full_txt)
    doi_mentions = []
    if avoid_numbers(find_str, full_txt):
        pass
    else:
        # Extract one DOI at a time
        while find_str in full_txt:
            snippet_nohtml = bs4.BeautifulSoup(
                full_txt, features="html.parser").get_text()
            str_location = snippet_nohtml.find(find_str)

            # Construct doi from string
            doi_mention = build_doi(snippet_nohtml, str_location)
            if doi_mention is not None:
                doi_mentions.append(doi_mention)

            # Remove find_str instance, reset full_txt
            full_txt = snippet_nohtml[
                :str_location
                ] + snippet_nohtml[str_location+6:]

        # remove dups
        doi_mentions = list(set(doi_mentions))

    return doi_mentions


def avoid_numbers(search_term, full_txt):
    """Check if string contains number substrings.

    Returns
    ----------
    True
        full_txt contains any of the search terms to avoid processing
    False
        full_txt does not contain any search terms to avoid
    """
    avoid1 = f" {search_term} "
    avoid2 = f" {search_term},"
    avoid3 = f" {search_term}."
    avoid4 = f" -{search_term}"
    avoid = [avoid1, avoid2, avoid3, avoid4]

    if any(x in full_txt for x in avoid):
        return True
    else:
        return False


def clean_unicode(full_txt):
    """Deal with some escaped unicode issues.

    Notes
    ----------
    Short term solution, reported to xDD
    """
    full_txt = re.sub(
        r"\u200b|\u2009|\u200a|\xa0",
        "",
        full_txt,
    )
    return full_txt


def build_doi(snippet, str_location):
    """Deal with issues from xDD doc parsing.

    Parameters
    ----------
    snippet: str
        string of unstructured text
    str_location: int
        index value of where text of interest starts
    """
    # '10.5066'= 7 chars, + 8 for unique ID, + 3 for " " or "/"
    doi_component = snippet[
                    str_location: (str_location + 18)
                ]

    # remove symbols and spaces
    doi_component_clean = re.sub(
        r"\ |\?|\.|\!|\/|\;|\:|\|<|>|\)|\(|,|\[|\]|\〉",
        "",
        doi_component,
    )

    # rebuilds doi with proper structure
    doi_rebuild = (
        doi_component_clean[0:2]
        + "."
        + doi_component_clean[2:6]
        + "/"
        + doi_component_clean[6:14]
                )

    if len(doi_rebuild.strip()) == 16:
        doi_mention = doi_rebuild
    else:
        doi_mention = None

    return doi_mention


# def doi_formatting(input_doi):
#     """Reformat loosely structured DOIs.

#     Currently only doing simplistic removal of 2 common http prefix
#     and changing case to upper.
#     End DOI should be in format NN.NNNN/*, not as url

#     Parameters
#     ----------
#     input_doi: str

#     """
#     input_doi = input_doi.upper()
#     if str(input_doi).startswith("HTTPS://DOI.ORG/"):
#         formatted_doi = input_doi[16:]  # Remove URL prefix
#     elif str(input_doi).startswith("HTTP://DX.DOI.ORG/"):
#         formatted_doi = input_doi[18:]
#     else:
#         formatted_doi = str(input_doi)
#     return formatted_doi
