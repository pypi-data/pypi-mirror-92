from jinja2 import Environment, PackageLoader

from django.template import Template, Context
from django.test import TestCase

from pipeline.jinja2 import PipelineExtension

from tests.utils import pipeline_settings


class JinjaTest(TestCase):
    def setUp(self):
        self.env = Environment(extensions=[PipelineExtension],
                               loader=PackageLoader('pipeline', 'templates'))

    def test_no_package(self):
        template = self.env.from_string(u"""{% stylesheet "unknow" %}""")
        self.assertEqual(u'', template.render())
        template = self.env.from_string(u"""{% javascript "unknow" %}""")
        self.assertEqual(u'', template.render())

    def test_package_css(self):
        template = self.env.from_string(u"""{% stylesheet "screen" %}""")
        self.assertEqual(u'<link href="/static/screen.css" rel="stylesheet" type="text/css" />', template.render())

    @pipeline_settings(PIPELINE_ENABLED=False)
    def test_package_css_disabled(self):
        template = self.env.from_string(u"""{% stylesheet "screen" %}""")
        self.assertEqual(u'''<link href="/static/pipeline/css/first.css" rel="stylesheet" type="text/css" />
<link href="/static/pipeline/css/second.css" rel="stylesheet" type="text/css" />
<link href="/static/pipeline/css/urls.css" rel="stylesheet" type="text/css" />''', template.render())

    def test_package_js(self):
        template = self.env.from_string(u"""{% javascript "scripts" %}""")
        self.assertEqual(u'<script type="text/javascript" src="/static/scripts.js" charset="utf-8"></script>', template.render())

    def test_package_js_async(self):
        template = self.env.from_string(u"""{% javascript "scripts_async" %}""")
        self.assertEqual(u'<script async type="text/javascript" src="/static/scripts_async.js" charset="utf-8"></script>', template.render())

    def test_package_js_defer(self):
        template = self.env.from_string(u"""{% javascript "scripts_defer" %}""")
        self.assertEqual(u'<script defer type="text/javascript" src="/static/scripts_defer.js" charset="utf-8"></script>', template.render())

    def test_package_js_async_defer(self):
        template = self.env.from_string(u"""{% javascript "scripts_async_defer" %}""")
        self.assertEqual(u'<script async defer type="text/javascript" src="/static/scripts_async_defer.js" charset="utf-8"></script>', template.render())


class DjangoTest(TestCase):
    def render_template(self, template):
        return Template(template).render(Context())

    def test_compressed_empty(self):
        rendered = self.render_template(u"""{% load pipeline %}{% stylesheet "unknow" %}""")
        self.assertEqual(u'', rendered)

    def test_compressed_css(self):
        rendered = self.render_template(u"""{% load pipeline %}{% stylesheet "screen" %}""")
        self.assertEqual(u'<link href="/static/screen.css" rel="stylesheet" type="text/css" media="all" />', rendered)

    def test_compressed_css_media(self):
        rendered = self.render_template(u"""{% load pipeline %}{% stylesheet "screen_media" %}""")
        self.assertEqual(u'<link href="/static/screen_media.css" rel="stylesheet" type="text/css" media="screen and (min-width:500px)" />', rendered)

    def test_compressed_css_title(self):
        rendered = self.render_template(u"""{% load pipeline %}{% stylesheet "screen_title" %}""")
        self.assertEqual(u'<link href="/static/screen_title.css" rel="stylesheet" type="text/css" media="all" title="Default Style" />', rendered)

    def test_compressed_js(self):
        rendered = self.render_template(u"""{% load pipeline %}{% javascript "scripts" %}""")
        self.assertEqual(u'<script type="text/javascript" src="/static/scripts.js" charset="utf-8"></script>', rendered)

    def test_compressed_js_async(self):
        rendered = self.render_template(u"""{% load pipeline %}{% javascript "scripts_async" %}""")
        self.assertEqual(u'<script async type="text/javascript" src="/static/scripts_async.js" charset="utf-8"></script>', rendered)

    def test_compressed_js_defer(self):
        rendered = self.render_template(u"""{% load pipeline %}{% javascript "scripts_defer" %}""")
        self.assertEqual(u'<script defer type="text/javascript" src="/static/scripts_defer.js" charset="utf-8"></script>', rendered)

    def test_compressed_js_async_defer(self):
        rendered = self.render_template(u"""{% load pipeline %}{% javascript "scripts_async_defer" %}""")
        self.assertEqual(u'<script async defer type="text/javascript" src="/static/scripts_async_defer.js" charset="utf-8"></script>', rendered)
