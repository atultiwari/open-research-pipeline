from check_links import URL_RE


def test_url_regex_stops_at_backtick_pipe_and_brackets():
    text = "See `https://a.org/x` | https://b.org/y| [c](https://c.org/z) <https://d.org/w>"
    assert URL_RE.findall(text) == ["https://a.org/x", "https://b.org/y", "https://c.org/z", "https://d.org/w"]
