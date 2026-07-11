import pytest
from django.test import RequestFactory, override_settings

from wger.utils.url import make_absolute_url


# Verifica comportamento de make_absolute_url quando SITE_URL está configurado
# e quando a URL já é absoluta.
@pytest.mark.parametrize(
    "path,expected",
    [
        ("/foo", "https://example.com/foo"),
        ("foo/bar", "https://example.com/foo/bar"),
        ("https://already.absolute/path", "https://already.absolute/path"),
    ],
)
@override_settings(SITE_URL="https://example.com")
def test_make_absolute_url_with_site_url(path, expected):
    assert make_absolute_url(path) == expected


# Verifica que make_absolute_url usa request.build_absolute_uri() quando um request
# é fornecido, preservando o host do request.
def test_make_absolute_url_with_request():
    request = RequestFactory().get("/unused")
    result = make_absolute_url("/bar", request)
    assert result == "http://testserver/bar"
