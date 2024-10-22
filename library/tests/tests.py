from django.test import TestCase

from ..models import Book  # Remplace par ton modèle réel
from django.urls import reverse

class BookModelTest(TestCase):

    def setUp(self):
        # Initialiser des données de test
        self.book = Book.objects.create(title='Django for Beginners')

    def test_book_title(self):
        # Test unitaire pour vérifier le titre du livre
        self.assertEqual(self.book.title, 'Django for Beginners')
    def test_view_url_exists(self):
            response = self.client.get(reverse('book_list'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'library/book_list.html')