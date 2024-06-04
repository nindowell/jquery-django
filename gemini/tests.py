from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Favorited

# Create your tests here.


class PostModelTest(TestCase):

    def setUp(self):
        self.post = Post.objects.create(
            title="Test Post",
            title_ru="Тест пост",
            content="This is a test post content."
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.title_ru, "Тест пост")
        self.assertEqual(self.post.content, "This is a test post content.")
        self.assertTrue(self.post.date_created)

    def test_post_str_method(self):
        self.assertEqual(str(self.post), "Test Post")


class FavoritedModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title="Test Post",
            content="Test post content."
        )
        self.favorited = Favorited.objects.create(user=self.user, post=self.post)

    def test_favorited_creation(self):
        self.assertEqual(self.favorited.user, self.user)
        self.assertEqual(self.favorited.post, self.post)
        self.assertTrue(self.favorited.date_added)


class ToggleFavoriteViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title="Test post",
            content="Test post content."
        )

    def test_toggle_favorite_add(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('toggle_favorite', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'is_favorite': True})
        self.assertTrue(Favorited.objects.filter(user=self.user, post=self.post).exists())

    def test_toggle_favorite_remove(self):
        self.client.login(username='testuser', password='12345')
        Favorited.objects.create(user=self.user, post=self.post)
        response = self.client.post(reverse('toggle_favorite', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'is_favorite': False})
        self.assertFalse(Favorited.objects.filter(user=self.user, post=self.post).exists())

    def test_toggle_favorite_invalid_method(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('toggle_favorite', args=[self.post.id]))
        # returns 405 invalid method
        self.assertEqual(response.status_code, 405)
