#!/usr/bin/env python
"""Tests for `publink` package."""

from publink import publink


def test_resolve_doi():
    """Ensure bad url fails."""
    bad_doi = 'this_is_a_bad_doi'
    assert publink.resolve_doi(bad_doi) is False
