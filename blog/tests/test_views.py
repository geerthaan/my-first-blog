"""
 run tests (webserver is not required to run, start  venv of course ):
 python manage.py test --verbosity 2

create fixture:
3 lines copy each line one by one,  to console, to append the whole line
don't copy the 3 lines at one once to console (to avoid errors)

python manage.py dumpdata --format=json --natural-foreign
--natural-primary -e contenttypes -e auth.Permission
--indent 4 > blog/fixtures/testdata.json

https://docs.djangoproject.com/en/2.1/topics/testing/tools/
see info about client(dummy webbrowser)
"""
from django.core.management import call_command

# from django.contrib.auth.models import AnonymousUser, User

from django.test import TestCase

from django.test import Client

from django.http import HttpRequest

from django.urls import reverse

from django.utils import timezone

from .. import views
from .. import models
from .. models import Post


# Create your tests here.

class HomePageTests(TestCase):
    # def setUp(self):
    # Set up data per TestCase, so runs  per testcase
    #     call_command('loaddata', './blog/fixtures/testdata.json', verbosity=0)
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase, so runs just once, at the start
        call_command('loaddata', './blog/fixtures/testdata.json', verbosity=0)

    # testing of the views
    def test_a1_home_page_status_code(self):
        response = self.client.get('/')
        path = response.request['PATH_INFO']
        print(path)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(path, "/")

    def test_a2_view_url_by_name_post_list(self):
        response = self.client.get(reverse('post_list'))
        path = response.request['PATH_INFO']
        print(path)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(path, "/")

    def test_a3_view_url_by_name_post_detail(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': 1}))
        path = response.request['PATH_INFO']
        print(path)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(path, "/post/1/")

    def test_a4_view_url_by_name_post_new(self):
        response = self.client.get(reverse('post_new'))
        path = response.request['PATH_INFO']
        print(path)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(path, "/post/new/")

    def test_a5_view_url_by_name_post_edit(self):
        response = self.client.get(reverse('post_edit', kwargs={'pk': 1}))
        path = response.request['PATH_INFO']
        print(path)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(path, "/post/1/edit/")

    def test_a6_view_url_by_name_draft_list(self):
        response = self.client.get(reverse('post_draft_list'))
        path = response.request['PATH_INFO']
        print(path)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(path, "/drafts/")

    # created a draft, that has pk 27 and created a fixture again,
    #  that contained that pk record
    def test_a6_view_url_by_name_publish(self):
        response = self.client.get(reverse('post_publish', kwargs={'pk': 27}))
        path = response.request['PATH_INFO']
        print(path)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(path, "/post/27/publish/")

    def test_a6_view_url_by_name_remove(self):
        response = self.client.get(reverse('post_remove', kwargs={'pk': 27}))
        path = response.request['PATH_INFO']
        print(path)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(path, "/post/27/remove/")

