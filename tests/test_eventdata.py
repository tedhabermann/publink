"""Tests for `xdd_search` package."""

from publink import eventdata
import validators

s = eventdata.SearchEventdata('10.5066/F7PG1PWZ', search_type="doi")
s.build_query_url()

response_data = [
    {'license': 'https://creativecommons.org/publicdomain/zero/1.0/',
     'terms': 'https://doi.org/10.13003/CED-terms-of-use',
     'obj_id': 'https://doi.org/10.5066/f7fj2dwj',
     'subj_id': 'https://en.wikipedia.org/wiki/Sea_otter',
     'id': 'ae3bc458-e865-49a3-90ae-bae76a8b500b',
     'relation_type_id': 'references'
     },
    {'license': 'https://doi.org/10.13003/CED-terms-of-use',
     'obj_id': 'https://doi.org/10.5066/F7GB2257',
     'subj_id': 'https://doi.org/10.1007/s10040-016-1406-y',
     'id': '6cbe2817-1e54-42dd-929e-8444ada767bc',
     'terms': 'https://doi.org/10.13003/CED-terms-of-use',
     'source_id': 'crossref',
     'relation_type_id': 'references'
     },
    {'license': 'https://creativecommons.org/publicdomain/zero/1.0/',
     'terms': 'https://doi.org/10.13003/CED-terms-of-use',
     'obj_id': 'https://doi.org/10.5066/f7wh2n65',
     'subj_id': 'https://www.usgs.gov/news/stitching-together-new-digital-geologic-quilt-united-states',
     'id': '696b6c1f-7dfe-4b5d-be4b-dfc8d123cb47',
     'relation_type_id': 'discusses'
     }
]


def test_build_query_url():
    """Validate query url."""
    url = s.search_url
    assert validators.url(url)


def test_get_related_dois():
    """Ensure expected related data is returned.

    Only return information where both pub_doi and
    search_term are dois.
    Only return information that has relation_type_id
    of references.

    """
    t = eventdata.GetRelated(response_data)
    t.get_related_dois()
    expected = [{"event_id": "2817-1e54-42dd-929e-8444ada767bc",
                 "pub_doi": "10.1007/s10040-016-1406-y",
                 "search_term": "10.5066/F7GB2257",
                 "source": "crossref"
                 }]
    related = t.related_dois.sort()
    assert related == expected.sort()
