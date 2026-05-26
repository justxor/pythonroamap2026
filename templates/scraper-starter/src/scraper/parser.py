"""HTML-парсинг через selectolax (lexbor)."""
from __future__ import annotations

from selectolax.parser import HTMLParser


def extract_title(html: str) -> str | None:
    tree = HTMLParser(html)
    node = tree.css_first("title")
    return node.text(strip=True) if node else None


def extract_text(html: str, selector: str) -> list[str]:
    tree = HTMLParser(html)
    return [n.text(strip=True) for n in tree.css(selector)]


def extract_attrs(html: str, selector: str, attr: str) -> list[str]:
    tree = HTMLParser(html)
    return [
        n.attributes[attr]
        for n in tree.css(selector)
        if attr in n.attributes and n.attributes[attr] is not None
    ]
