from ontolocy.models.url import URLNode, UrlRedirectsToUrl


def test_url():
    my_url = URLNode(url="http://example.com/hello")

    assert str(my_url.url) == "http://example.com/hello"


def test_redirects_rel(use_graph):
    url1 = URLNode(url="http://example.com/foo")
    url1.merge()

    url2 = URLNode(url="http://example.com/bar")
    url2.merge()

    rel = UrlRedirectsToUrl(source=url1, target=url2)
    rel.merge()

    cypher = """
    MATCH (url1:URL)-[r:URL_REDIRECTS_TO_URL]->(url2:URL)
    WHERE url1.url = 'http://example.com/foo'
    RETURN COUNT(DISTINCT r)
    """

    result = use_graph.evaluate(cypher)

    assert result == 1
