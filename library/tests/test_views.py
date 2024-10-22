from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from library.models import Book


class AddBookViewTests(TestCase):
   
    def test_add_book_get(self):
        """
        Test if the `add_book` view returns the page with the form for GET access.
        """
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/add_book.html')


    def test_add_book_post_valid_data(self):
        """
        Test if a book is correctly added via a POST request with valid data.
        """
        data = {
            'title': 'Django for Beginners',
            'author': 'William S. Vincent',
            'description': 'A beginner\'s guide to Django framework.',
            'published_date': timezone.now().date(),
        }
        response = self.client.post(reverse('add_book'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.first().title, 'Django for Beginners')


    def test_add_book_post_invalid_data(self):
        """
       Test if a book is correctly added via a POST request with valid data.
        """
        data = {
            'title': '',  # empty input
            'author': '',
            'description': '',
            'published_date': '',
        }
        response = self.client.post(reverse('add_book'), data)
        self.assertEqual(response.status_code, 200)  # Stay on the same page with errors
        #self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertEqual(Book.objects.count(), 0)  # not book ad


    def test_add_book_template_used(self):
        """
        Test if the correct template is used for the `add_book` view.
        """
        response = self.client.get(reverse('add_book'))
        self.assertTemplateUsed(response, 'library/add_book.html')
