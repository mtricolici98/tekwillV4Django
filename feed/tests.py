from django.test import TestCase

from feed.models import Post


# Create your tests here.
class Test(TestCase):

    def test_post_add(self):
        self.assertEqual(Post.objects.count(), 0)
        self.client.post(
            '/feed/post/add',
            {'title': 'test title', 'content': 'test'}
        )
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().title, 'test title')
