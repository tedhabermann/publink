#!/usr/bin/env python
"""Tests for `publink` package."""

from publink import publink

search_terms1 = ('10.5066/P9LYUFRH')
p1 = publink.search_xdd(search_terms1)
p2 = publink.xdd_mentions(
    p1.response_data, p1.search_terms, is_doi=True
)


test_mentions = [{'pub_doi': '10.3133/OFR20191040',
                  'search_term': '10.5066/P9LYUFRH'},
                 {'pub_doi': '10.3133/OFR20191040',
                 'search_term': '10.5066/P9LYUFRH'},
                 {'pub_doi': '10.3133/OFR20191040',
                 'search_term': '10.5066/F7PG1PWZ'},
                 {'search_term': '10.5066/F7PG1PWZ'}
                 ]


def test_search_xdd():
    """Test information is returned in search xdd.

    Uses a DOI that we know had 1 response on 7/31/2020.

    """
    assert p1.response_hits >= 1


def test_xdd_mentions():
    """Test mentions.

    Uses a DOI that we know had 2 mentions on 7/31/2020.

    """
    assert len(p2.mentions) >= 2


def test_to_related_identifiers():
    """Test reformat of identifiers."""
    to_rel = publink.to_related_identifiers(test_mentions)
    expected_related = {'doi': '10.5066/F7PG1PWZ',
                        'identifier': 'https://doi.org/10.5066/F7PG1PWZ',
                        'related-identifiers': [
                            {'relation-type-id': 'IsCitedBy',
                             'related-identifier': 'https://doi.org/10.3133/OFR20191040'
                             }]}
    t = [i for i in to_rel if i['doi'] == '10.5066/F7PG1PWZ'][0]
    assert t['related-identifiers'] == expected_related['related-identifiers']
    assert t['identifier'] == expected_related['identifier']


def test_validate_dois():
    """Test validation of dois."""
    test_dois = ['10.5066/F79021VS',
                 'baddoi',
                 '10.5066/F79021VS',
                 '10.5066/1111111'
                 ]
    good_dois, bad_dois = publink.validate_dois(test_dois)
    assert good_dois == ['10.5066/F79021VS']
    assert set(bad_dois) == set(['baddoi', '10.5066/1111111'])


def test_resolve_doi():
    """Ensure bad url fails."""
    bad_doi = "this_is_a_bad_doi"
    good_doi = "10.5066/F79021VS"
    assert publink.resolve_doi(bad_doi) is False
    assert publink.resolve_doi(good_doi) is True


def test_get_unique_pairs():
    """Test unique pairs.

    Test has one duplicate and one missing pub_doi.
    Expect to get 2 unique pairs.

    """
    expected_out = [{'pub_doi': '10.3133/OFR20191040',
                     'search_term': '10.5066/P9LYUFRH'},
                    {'pub_doi': '10.3133/OFR20191040',
                     'search_term': '10.5066/F7PG1PWZ'}
                    ]
    test_out = publink.get_unique_pairs(test_mentions)
    assert [i for i in test_out if i not in expected_out] == []
    assert len(expected_out) == len(test_out)


def test_doi_formatting():
    """Test doi formatting."""
    test_dois = ['10.5066/P9LYUFRH', '10.5066/p9lyufrh',
                 '10.5066/P9LY UFRH', 'DOI:10.5066/P9LYUFRH',
                 'HTTPS://DOI.ORG/DOI:10.5066/p9lyufrh',
                 'HTTPS://DX.DOI.ORG/DOI:10.5066/p9lyufrh',
                 'HTTP://DOI.ORG/DOI:10.5066/p9lyufrh',
                 'HTTP://DX.DOI.ORG/DOI:10.5066/p9lyufrh',
                 'HTTPS://DOI.ORG/10.5066/p9lyufrh',
                 'HTTPS://DX.DOI.ORG/10.5066/p9lyufrh',
                 'HTTP://DOI.ORG/10.5066/p9lyufrh',
                 'HTTP://DX.DOI.ORG/10.5066/p9ly ufrh']

    format_doi = '10.5066/P9LYUFRH'
    for test in test_dois:
        test_out = publink.doi_formatting(test)
        assert test_out == format_doi
