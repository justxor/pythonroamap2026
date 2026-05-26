from scraper.parser import extract_attrs, extract_text, extract_title


def test_extract_title() -> None:
    html = "<html><head><title>Hello World</title></head><body></body></html>"
    assert extract_title(html) == "Hello World"


def test_extract_title_missing() -> None:
    assert extract_title("<html><body></body></html>") is None


def test_extract_text() -> None:
    html = '<ul><li class="x">a</li><li class="x">b</li></ul>'
    assert extract_text(html, "li.x") == ["a", "b"]


def test_extract_attrs() -> None:
    html = '<a href="/1">one</a><a href="/2">two</a>'
    assert extract_attrs(html, "a", "href") == ["/1", "/2"]
