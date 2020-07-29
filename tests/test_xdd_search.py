"""Tests for `xdd_search` package."""

from publink import xdd_search
import validators

s = xdd_search.SearchXdd()
s.all_search_terms()
s.build_query_urls()

test_response = {'search_terms': ['10.5066/F7K935KT'],
                 'response_data': [
                     {'_gddid': '585b4a6ccf58f1a722da91ea',
                      'doi': '10.1002/esp.4023',
                      'out_doi': '10.1002/ESP.4023',
                      'highlight': [
                          'Greene S. 2015. USGS Dam Removal Science Database. DOI:10.5066/F7K935KT. Brandt SA.',
                          'Science Database. DOI:10.5066/F7K935KT. Brandt SA. 2000. Classification of geomorphological'
                      ]},
                     {'_gddid': '57d99165cf58f191c21a5829',
                      'out_doi': '',
                      'highlight': [
                          'U.S. Geological Survey data release, http://doi.org/10.5066/F7K935KT. Berners-Lee,',
                          'release, http://doi.org/10.5066/F7K935KT. Berners-Lee, T., 2006, Linked data, design'
                      ]}]
                 }

expected_exact_mentions = [{'xdd_id': '585b4a6ccf58f1a722da91ea',
                            'pub_doi': '10.1002/ESP.4023',
                            'search_term': '10.5066/F7K935KT',
                            'highlight': 'GREENE S. 2015. USGS DAM REMOVAL SCIENCE DATABASE. DOI:10.5066/F7K935KT. BRANDT SA.'},
                           {'xdd_id': '585b4a6ccf58f1a722da91ea',
                            'pub_doi': '10.1002/ESP.4023',
                            'search_term': '10.5066/F7K935KT',
                            'highlight': 'SCIENCE DATABASE. DOI:10.5066/F7K935KT. BRANDT SA. 2000. CLASSIFICATION OF GEOMORPHOLOGICAL'},
                           {'xdd_id': '57d99165cf58f191c21a5829',
                            'pub_doi': '',
                            'search_term': '10.5066/F7K935KT',
                            'highlight': 'U.S. GEOLOGICAL SURVEY DATA RELEASE, HTTP://DOI.ORG/10.5066/F7K935KT. BERNERS-LEE,'},
                           {'xdd_id': '57d99165cf58f191c21a5829',
                            'pub_doi': '',
                            'search_term': '10.5066/F7K935KT',
                            'highlight': 'RELEASE, HTTP://DOI.ORG/10.5066/F7K935KT. BERNERS-LEE, T., 2006, LINKED DATA, DESIGN'}]

expected_usgs_mentions = [{'xdd_id': '585b4a6ccf58f1a722da91ea',
                           'pub_doi': '10.1002/ESP.4023',
                           'search_term': '10.5066/F7K935KT',
                           'certainty': 'most certain',
                           'highlight': 'GREENE S. 2015. USGS DAM REMOVAL SCIENCE DATABASE. DOI:10.5066/F7K935KT. BRANDT SA.'},
                          {'xdd_id': '585b4a6ccf58f1a722da91ea',
                           'pub_doi': '10.1002/ESP.4023',
                           'search_term': '10.5066/F7K935KT',
                           'certainty': 'most certain',
                           'highlight': 'SCIENCE DATABASE. DOI:10.5066/F7K935KT. BRANDT SA. 2000. CLASSIFICATION OF GEOMORPHOLOGICAL'},
                          {'xdd_id': '57d99165cf58f191c21a5829',
                           'pub_doi': '',
                           'search_term': '10.5066/F7K935KT',
                           'certainty': 'most certain',
                           'highlight': 'U.S. GEOLOGICAL SURVEY DATA RELEASE, HTTP://DOI.ORG/10.5066/F7K935KT. BERNERS-LEE,'},
                          {'xdd_id': '57d99165cf58f191c21a5829',
                           'pub_doi': '',
                           'search_term': '10.5066/F7K935KT',
                           'certainty': 'most certain',
                           'highlight': 'RELEASE, HTTP://DOI.ORG/10.5066/F7K935KT. BERNERS-LEE, T., 2006, LINKED DATA, DESIGN'}]

test_snippets = [
    {
        "snippet": "data release. https://doi. org/10.5066/f7pg1pwz Lehtonen, J.",
        "correct_doi": ["10.5066/f7pg1pwz"],
    },
    {
        "snippet": " USGS ScienceBase https://doi.org/10.5066/ f7fx7aaa (Dibble, Sabo,",
        "correct_doi": ["10.5066/f7fx7aaa"],
    },
    {
        "snippet": ". Retrieved from https://doi.org/10.5066/f7fx7bbb Douglas, M. E., &",
        "correct_doi": ["10.5066/f7fx7bbb"],
    },
    {
        "snippet": "https://doi.org/10.5066/f7fx7ccc Douglas, M. E., & Marsh, P. C.",
        "correct_doi": ["10.5066/f7fx7ccc"],
    },
    {
        "snippet": ". Retrieved from https: //doi.org/10.5066/f7fx7ddd",
        "correct_doi": ["10.5066/f7fx7ddd"],
    },
    {
        "snippet": ". Retrieved from (https://doi.org/10.5066/f7fx7eee) Douglas, M. E.",
        "correct_doi": ["10.5066/f7fx7eee"],
    },
    # note html is taken out before this step, this test will fail
    # {'snippet':
    #  '. Retrieved from <https://doi.org/10.5066/f7fx7fff> Douglas, M. E.'
    #  'correct_doi': ['10.5066/f7fx7fff']
    #  },
    {
        "snippet": "from (https://doi.org/10.5066/f7fx7ggg) Doi10.5066/f7pg1pwz 8686876",
        "correct_doi": ["10.5066/f7pg1pwz", "10.5066/f7fx7ggg"],
    },
    {"snippet": ". Retrieved from 10.5066, M. E., P. C.", "correct_doi": []},
]

expected_terms = ["10.5066",
                  "1 0.5066",
                  "10 .5066",
                  "10. 5066",
                  "10.5 066",
                  "10.50 66",
                  "10.506 6",
                  ]


def test_all_search_terms():
    """Assert correct list created."""
    assert sorted(expected_terms) == sorted(s.search_terms)


def test_build_query_urls():
    """Validate query urls."""
    for url in s.search_urls:
        assert validators.url(url)


def test_query_xdd():
    """Assert number of records equals expected hits."""
    s.build_query_urls()
    # Grab first search term
    s.next_url = s.search_urls[0]
    s.query_xdd()
    if s.response_status == "success":
        assert s.response_hits == len(s.response_data)


def test_get_exact_mention():
    """Verify exact mention extraction doesn't fail and correct count."""
    t = xdd_search.GetMentions(test_response['response_data'], test_response['search_terms'])
    t.get_exact_mention(is_doi=True)
    t.mentions == expected_exact_mentions


def test_get_usgs_doi_mentions():
    """Verify usgs mention extraction doesn't fail and correct count."""
    t = xdd_search.GetMentions(test_response['response_data'], test_response['search_terms'])
    t.search_terms = expected_terms
    t.get_usgs_doi_mentions()
    assert t.mentions == expected_usgs_mentions


def test_clean_highlight():
    """Test removal of unicode issues from snippet."""
    in_snippet = "U.S. Geological Survey data release,\xa0https://doi.org/10.50 66/F7639MZX.   References Cited\u2003\u2003183  Capel"
    out_snippet = "U.S. GEOLOGICAL SURVEY DATA RELEASE,HTTPS://DOI.ORG/10.5066/F7639MZX.   REFERENCES CITED183  CAPEL"
    assert xdd_search.clean_highlight(in_snippet, expected_terms) == out_snippet


def test_extract_usgs_doi():
    """Verify DOI extracted from string correctly."""
    prefix = "10.5066"
    for test in test_snippets:
        all_dois = []
        hl_words = test["snippet"].split(" ")
        have_prefix = list(set([hl_word for hl_word in hl_words if prefix in hl_word]))

        for mention in have_prefix:
            extract_doi = xdd_search.extract_usgs_doi(hl_words, mention)
            all_dois.append(extract_doi[0])
        assert test["correct_doi"].sort() == all_dois.sort()


def test_clean_unicode():
    """Test removal of unicode issues from snippet."""
    in_snippet = "U.S. Geological Survey data release,\xa0https://doi.org/10.5066/F7639MZX.   References Cited\u2003\u2003183  Capel"
    out_snippet = "U.S. Geological Survey data release,https://doi.org/10.5066/F7639MZX.   References Cited183  Capel"
    assert xdd_search.clean_unicode(in_snippet) == out_snippet


def test_get_pub_doi():
    """Verify DOI is extracted and doesn't fail if no DOI."""
    for ref in test_response['response_data']:
        assert xdd_search.get_pub_doi(ref) == ref['out_doi']
