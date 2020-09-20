from django.test import TestCase
from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Post


def home(request):
    blog = Post.objects.get(pk=1)
    return render(request, '', {'section': 'home', 'title': 'Albert Einstein'})


class PostTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = Post.objects.create(title='Albert Einstein')
    # fixtures = ['blog_data.json']

    def test_home(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['section'], 'home')
        self.assertEqual(response.context['post'].title, 'Albert Einstein')
