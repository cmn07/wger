# wger
from wger.utils.markdown import (
    render_markdown,
    sanitize_html,
)


# Verifica que render_markdown converte markdown básico para HTML mantendo apenas
# tags seguras permitidas.
def test_render_markdown_allows_basic_html_tags():
    content = '**bold** and _italic_'
    result = render_markdown(content)

    assert '<strong>bold</strong>' in result
    assert '<em>italic</em>' in result


# Verifica que render_markdown remove tags perigosas como <script> durante a
# renderização e sanitização.
def test_render_markdown_strips_disallowed_tags():
    content = "<script>alert('xss')</script>"
    result = render_markdown(content)

    assert '<script>' not in result
    assert result == ''


# Verifica que sanitize_html filtra HTML direto, permitindo apenas as tags
# básicas definidas na lista de permitidas.
def test_sanitize_html_allows_only_basic_tags():
    content = "<b>ok</b><iframe src='http://example.com'></iframe>"
    result = sanitize_html(content)

    assert '<b>ok</b>' in result
    assert '<iframe' not in result
