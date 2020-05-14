"""Tests for `xdd_search` package."""

import pytest
from publink import doi_tool
import json


def build_test_data(file_name):
    """Build test data from file.

    Parameters
    ----------
    file_name: str
        includes directory and extension example 'data.txt'
        Mock JSON representing a DOI's content, built in staging

    Returns
    ----------
    update_object: object
        object as defined by Class doi_tool.UpdateDoi

    """
    # Read stored DOI content (JSON) from txt file
    with open(file_name) as json_file:
        test_data = json.load(json_file)

    doi_to_update = test_data["doi"][4:]  # DOI no prefix
    related_dois = ['10.23706/1111111A', '10.5066/P9LYUFRH']

    update_object = doi_tool.UpdateDoi(
        doi_to_update, related_dois, session=None
        )
    update_object.doi_content = test_data
    update_object.relatedIdentifiers = update_object.doi_content[
        "relatedIdentifiers"
        ]
    return update_object


def test_all_related_empty():
    """Verify update JSON builds correctly with no relations initially.

    The target DOI initially has no built in relations to other DOIs.
    Asserts that both DOI relations were added to the target DOI content.

    """
    data = build_test_data("tests/empty_relations.txt")
    data.all_related()
    result = [{'relatedIdentifier': 'https://doi.org/10.23706/1111111A',
               'dataciteRelationType': 'IS_CITED_BY',
               'relatedIdentifierType': 'DOI'
               },
              {'relatedIdentifier': 'https://doi.org/10.5066/P9LYUFRH',
               'dataciteRelationType': 'IS_CITED_BY',
               'relatedIdentifierType': 'DOI'
               }]

    assert data.related_dois == ['10.23706/1111111A', '10.5066/P9LYUFRH']
    assert result == data.update_doi_json


def test_all_related_has_data():
    """Verify update JSON builds correctly with initial relations.

    Asserts that only one DOI was updated into the DOI
    content JSON.  The other DOI was already related to
    the target DOI.  This case also verifies that a third
    DOI ("10.3133/OFR20191040") was not altered
    in the process.

    """
    data = build_test_data("tests/has_relations.txt")
    data.all_related()
    result = [{'relatedIdentifier': 'https://doi.org/10.5066/P9LYUFRH',
               'dataciteRelationType': 'IS_CITED_BY',
               'relatedIdentifierType': 'DOI'
               },
              {'relatedIdentifier': 'https://doi.org/10.23706/1111111A',
               'dataciteRelationType': 'IS_DOCUMENTED_BY',
               'usgsRelationSubType': None,
               'relatedIdentifierType': 'DOI'
               },
              {'relatedIdentifier': 'https://doi.org/10.3133/OFR20191040',
               'dataciteRelationType': 'IS_CITED_BY',
               'usgsRelationSubType': None,
               'relatedIdentifierType': 'DOI'
               }]

    assert data.related_dois == ['10.5066/P9LYUFRH']
    assert result == data.update_doi_json
