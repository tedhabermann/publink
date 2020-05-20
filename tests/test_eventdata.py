"""Tests for `xdd_search` package."""

from publink import eventdata
import validators

s = eventdata.SearchEventdata('10.5066/F7PG1PWZ', search_type="doi")
s.build_query_url()


def test_build_query_url():
    """Validate query url."""
    url = s.search_url
    assert validators.url(url)
