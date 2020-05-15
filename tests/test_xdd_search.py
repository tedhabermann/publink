"""Tests for `xdd_search` package."""

from publink import xdd_search

s = xdd_search.SearchXdd()
s.all_search_terms()

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


def test_all_search_terms():
    """Assert correct list created."""
    expected = [
        "10.5066",
        "1 0.5066",
        "10 .5066",
        "10. 5066",
        "10.5 066",
        "10.50 66",
        "10.506 6",
    ]
    assert sorted(expected) == sorted(s.search_terms)


def test_query_xdd():
    """Assert number of records equals expected hits."""
    s.build_query_urls()
    # Grab first search term
    s.next_url = s.search_urls[0]
    s.query_xdd()
    if s.response_status == "success":
        assert s.response_hits == len(s.response_data)


def test_extract_usgs_doi():
    """Verify DOI extracted from string correctly."""
    prefix = "10.5066"
    for test in test_snippets:
        all_dois = []
        hl_words = test["snippet"].split(" ")
        have_prefix = list(
            set([hl_word for hl_word in hl_words if prefix in hl_word])
        )

        for mention in have_prefix:
            extract_doi = xdd_search.extract_usgs_doi(hl_words, mention)
            all_dois.append(extract_doi[0])
        assert test["correct_doi"].sort() == all_dois.sort()
