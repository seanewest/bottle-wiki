from hypothesis import given, strategies as st
from wsgi_intercept import requests_intercept, add_wsgi_intercept
import requests
import bottle
import webtest
import app

import pytest

"""
Scenarios:
    User visits / and is redirected to /index
    When /<pagename> has no content, a 404 page is displayed with a link to /<pagename>/edit
    /<pagename>/edit has a form for editing the content and changing the name
    User creates a new page
    User modifies a page
    User browses pages
"""
host, port = 'localhost', 80
url = 'http://{0}:{1}/'.format(host, port)

@pytest.fixture
def db(scope='function'):
    app.db = app.Wikidb(':memory:')
    yield

@pytest.fixture
def wsgi():
    requests_intercept.install()
    add_wsgi_intercept(host, port, bottle.default_app)
    yield
    requests_intercept.uninstall()

@given(slug=st.just(''))
def test_index(slug, wsgi, db):
    resp = requests.get(url+slug)
    assert resp.ok

def test_edit(wsgi, db):
    article = 'This is a test article'
    data = {'subject':'Test Subject', 'article':article}
    edit_resp = requests.post(url + 'edit', data=data, allow_redirects=False)
    assert edit_resp.ok
    assert edit_resp.headers['Location'] == 'http://localhost/' + data['subject']
    response = requests.get(url + 'test subject')
    assert article in response.text

def test_edit_post(db, monkeypatch):
    class Stub:
        forms = {'subject':"Test", 'article':"This is a test."}
    monkeypatch.setattr(app, 'request', Stub())
    with pytest.raises(bottle.HTTPResponse):
        app.edit()
