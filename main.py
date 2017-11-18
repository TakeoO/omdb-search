#!/usr/bin/env python
import os
import jinja2
import webapp2
import library.models
import urllib2
import urllib
import json
import math

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)

url = "http://www.omdbapi.com/?apikey=b7c1146a&s=%s&page=%s"


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):

        query = self.request.get("q")
        page = self.request.get("p")

        query = query.strip()

        if len(page) <= 0:
            page = 1

        page = int(page)
        if page < 1:
            page = 1

        results = {}
        foundRows = 0
        pages = 0
        if len(query) > 0:
            query = urllib.quote_plus(query)
            url = "http://www.omdbapi.com/?apikey=b7c1146a&s=%s&page=%s"
            url = url % (query, page)
            content = urllib2.urlopen(url=url).read()
            obj = json.loads(content)
            results = obj["Search"]
            foundRows = int(obj["totalResults"])
            pages = int(math.ceil(float(foundRows) / 10))

        return self.render_template("hello.html", {
            "results": results,
            "foundRows": foundRows,
            "page": page,
            "pages": pages,
            "query": query
        })


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler)
], debug=True)
