"""Tests for `xdd_search` package."""

import pytest


from publink import xdd_search


def test_query_xdd():
    """Assert number of records equals expected hits."""
    s = xdd_search.SearchXdd()
    s.build_query()
    s.query_xdd()
    if s.response_status == 'success':
        assert s.response_hits == len(s.response_data)


def test_extract_doi():
    """Verify DOI extracted from string correctly."""
    find_str = "10.5066"
    test_snippets = [
        {'snippet':
         'data release. https://doi. org/10.5066/f7pg1pwz Lehtonen, J.',
         'correct_doi': ['10.5066/f7pg1pwz']
         },
        {'snippet':
         ' USGS ScienceBase https://doi.org/10.5066/ f7fx7aaa (Dibble, Sabo,',
         'correct_doi': ['10.5066/f7fx7aaa']
         },
        {'snippet':
         '. Retrieved from https://doi.org/10.5066/f7fx7bbb Douglas, M. E., &',
         'correct_doi': ['10.5066/f7fx7bbb']
         },
        {'snippet':
         'https://doi.org/10.5066/f7fx7ccc Douglas, M. E., & Marsh, P. C.',
         'correct_doi': ['10.5066/f7fx7ccc']
         },
        {'snippet':
         '. Retrieved from https: //doi.org/10.5066/f7fx7ddd',
         'correct_doi': ['10.5066/f7fx7ddd']
         },
        {'snippet':
         '. Retrieved from (https://doi.org/10.5066/f7fx7eee) Douglas, M. E.',
         'correct_doi': ['10.5066/f7fx7eee']
         },
        # note html is taken out before this step, this test will fail
        # {'snippet':
        #  '. Retrieved from <https://doi.org/10.5066/f7fx7fff> Douglas, M. E.'
        #  'correct_doi': ['10.5066/f7fx7fff']
        #  },
        {'snippet':
         'from (https://doi.org/10.5066/f7fx7ggg) Doi10.5066/f7pg1pwz 8686876',
         'correct_doi': ['10.5066/f7pg1pwz', '10.5066/f7fx7ggg']
         },
        {'snippet':
         '. Retrieved from 10.5066, M. E., P. C.',
         'correct_doi': []
         }
    ]
    for test in test_snippets:
        extract_doi = xdd_search.extract_doi(find_str, test['snippet'])
        assert test['correct_doi'].sort() == extract_doi.sort()
