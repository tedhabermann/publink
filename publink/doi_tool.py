"""Update DOI with new related pubs."""

# Import packages
import os
import getpass
from usgs_datatools import doi as doi_tool


class UpdateDoi():
    """Class for updaing DOI relationships in USGS DOI Tool."""

    def __init__(self, doi, related_dois, session, doi_relation="IS_CITED_BY"):
        """Initialize object with DOI update information.

        Parameters
        ----------
        doi: str
            target doi with format 10.5066/UUUUUUUU where U refers to
            an upper case character
        related_dois: list of strings
            example ['10.3133/OFR20161069','10.3133/OFR2FFDS']
        session: object
            DOI Tool Session.
            This is to avoid opening a new session for each init
        doi_relation: str, default "IS_CITED_BY"
            More information and options at datacite

        """
        self.target_doi = str(doi).upper()
        self.related_dois = [str(i).upper() for i in related_dois]
        self.doi_relation = doi_relation
        self.session = session
        self.response_message = "No request made."
        self.find_doi = f"doi:{self.target_doi}"
        self.update_doi_json = []

    def get(self):
        """Get DOI info from USGS DOI Tool."""
        self.doi_content = self.session.get_doi(self.find_doi)
        self.relatedIdentifiers = self.doi_content["relatedIdentifiers"]

    def all_related(self):
        """Build JSON of all relations to target DOI.

        Appends all dictionaries of relations of DOIs
        to target DOI.

        """
        if len(self.relatedIdentifiers) == 0:
            self.build_update_json()
        else:
            content_related_dois = list(set([
                i['relatedIdentifier'] for i
                in self.relatedIdentifiers
                ]))
            keep_dois = []
            for related_doi in self.related_dois:
                doi_url = f"https://doi.org/{related_doi}"
                if doi_url not in content_related_dois:
                    keep_dois.append(related_doi)
            self.related_dois = keep_dois
            if len(self.related_dois) > 0:
                self.build_update_json()
                self.update_doi_json.extend(self.relatedIdentifiers)
            else:
                self.update_doi_json = None
                self.response_message = "All relations already accounted for."

    def build_update_json(self):
        """Build dictionary for new DOI relation.

        Build dictionary of information to allow for update
        to the target DOI in the DOI tool.

        """
        for related_doi in self.related_dois:
            doi_url = f"https://doi.org/{related_doi}"
            update_json = {
                "relatedIdentifier": (doi_url),
                "dataciteRelationType": self.doi_relation,
                "relatedIdentifierType": "DOI"
            }
            self.update_doi_json.append(update_json)

    def update_doi_relations(self):
        """Update DOI with relationships to publication DOIs."""
        if self.update_doi_json is not None:
            self.doi_content["relatedIdentifiers"] = self.update_doi_json
            r = self.session.doi_update(self.doi_content)
            if "error" in r:
                self.response_message = "Update error."
            else:
                self.response_message = "Update successful."


def session(session_env="staging"):
    """Initiate DOI session.

    User must initiate session before using doi_tool module.

    """
    if os.getenv("DOI_USER") is not None and os.getenv("DOI_PW") is not None:
        user_name = os.getenv("DOI_USER")
        password = os.getenv("DOI_PW")
    else:
        user_name = input("User name: ")
        password = getpass.getpass(prompt="Password: ")

    local_doi_session = doi_tool.DoiSession(env=session_env)
    local_doi_session.doi_authenticate(user_name, password)
    return local_doi_session
