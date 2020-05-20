"""Extract info from crossref eventdata (https://www.eventdata.crossref.org)."""

# Import packages
import requests


class SearchEventdata:
    """Class allowing for searching of crossref eventdata by DOI."""

    def __init__(self, search_term, search_type="doi", mailto=""):
        """Initialize search eventdata obj.

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

        Notes
        ----------
        In dev this api fails more times than succeeds and may require
        several attempts before getting successful return

        """
        self.base_url = "https://api.eventdata.crossref.org/v1/events?"
        self.mailto = mailto
        self.search_term = str(search_term).upper()
        self.search_type = str(search_type).lower()
        self.search_url = None
        self.response_hits = 0
        self.response_data = []
        self.response_status = "error"
        self.response_message = "No request made."

    def build_query_url(self, rows=10000):
        """Build eventdata query url to search user defined DOI.

        Results
        ----------
        self.search_urls: list of strings
            List of urls to query.

        """
        if self.search_type == 'doi':
            q = f"mailto={self.mailto}&rows={rows}&obj-id={self.search_term}"
            self.search_url = f"{self.base_url}{q}"
        elif self.search_type == 'doi_prefix':
            q = f"mailto={self.mailto}&rows={rows}&obj-id.prefix={self.search_term}"
            self.search_url = f"{self.base_url}{q}"
        else:
            self.response_message = "Incorrect search type"

    def get_data(self):
        """Get data from eventdata."""
        if self.search_url is not None:
            self.next_url = self.search_url
            self.query_eventdata()

    def query_eventdata(self):
        """Query eventdata."""
        while self.next_url is not None:
            r = requests.get(self.next_url)
            if r.status_code == 200 and r.json()['status'] == 'ok':
                json_response = r.json()
                self.response_hits = json_response['message']['total-results']
                page_data = json_response['message']['events']
                self.response_data.extend(page_data)
                if json_response["message"]["next-cursor"] is None:
                    self.next_url = None
                else:
                    next = json_response["message"]["next-cursor"]
                    self.next_url = f"{self.search_url}&cursor={next}"

                self.response_status = "success"
                self.response_message = "Successful response."
            else:
                self.next_url = ""
                if r.status_code == 200 and r.json()['status'] == 'failed':
                    self.response_status = "no data"
                    self.response_message = f"failed request: {r.json()['message']}"
                elif r.status_code != 200:
                    self.response_status = "error"
                    self.response_message = f"failed request: status code {r.status_code}"
                    break
                else:
                    self.response_status = "error"
                    self.response_message = "Unknown error."
                    break


class GetRelated:
    """Class extracting relations from eventdata response."""

    def __init__(self, eventdata_data):
        """Initialize object to get mentions of search term from eventdata.

        Parameters
        ----------
        eventdata_response: json
            Response from eventdata query.  SearchEventdata response_data

        """
        self.events = eventdata_data

    def get_related_dois(self):
        """Extract related DOIs from eventdata.

        Returns
        ----------
        self.related_dois: list of dict
            includes publication xDD id, publication DOI and search term
            e.g. [{'eventdata_id':'66b96593-8b0a-477a-a283-5778ce75fcc5',
                   'related_doi':'10.1111/eva.12645',
                   'doi':'10.6084/m9.figshare.5234068'
                   }]

        """
        self.related_dois = []
        for event in self.events:
            doi_prefix = "https://doi.org/"
            if doi_prefix in event["obj_id"] and \
               doi_prefix in event["subj_id"] and \
               event['relation_type_id'] == 'references':

                related = {"event_id": event["id"],
                           "pub_doi": event["subj_id"].split(doi_prefix)[1],
                           "search_term": event["obj_id"].split(doi_prefix)[1],
                           "source": event["source_id"]}
                self.related_dois.append(related)
