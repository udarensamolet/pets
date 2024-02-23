from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import MagicMock

from petstagram.photos.models import Photo
from petstagram.common.forms import CommentForm
from petstagram.photos.views import add_photo


class PhotoViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test_password')

        self.photo = Photo.objects.create(user=self.user)

    def test_add_photo_view(self):
        # Create a mock form with valid data
        form_data = {
            'caption': 'Test Caption',
            'image': MagicMock(name='uploaded_image', spec=['name', 'size']),
        }
        request = self.factory.post(reverse('add-photo'), form_data)
        request.user = self.user

        self.client.login(username='testuser', password='testpassword')

        response = add_photo(request)

        # Check if the view redirects to the home page upon successful form submission
        self.assertRedirects(response, reverse('home'))

        # Check if the photo is created and associated with the logged-in user
        self.assertTrue(Photo.objects.filter(user=self.user, caption='Test Caption').exists())

        # Check if the form is not present in the context after successful submission
        self.assertNotIn('form', response.context)

    def test_add_photo_view_invalid_form(self):
        # Create a mock form with invalid data
        form_data = {
            'caption': '',  # Invalid: Caption is required
            'image': MagicMock(name='uploaded_image', spec=['name', 'size']),
        }
        request = self.factory.post(reverse('add-photo'), form_data)
        request.user = self.user

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the add_photo view with the mock form data
        response = add_photo(request)

        # Check if the view renders the template with the form and errors
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue(response.context['form'].errors)

        # Check if the photo is not created with invalid form data
        self.assertFalse(Photo.objects.filter(user=self.user).exists())

    def test_delete_photo_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the delete_photo view for the test photo
        response = self.client.get(reverse('delete-photo', args=[self.photo.pk]))

        # Check if the view redirects to the home page after deleting the photo
        self.assertRedirects(response, reverse('home'))

        # Check if the photo is deleted
        self.assertFalse(Photo.objects.filter(pk=self.photo.pk).exists())

    # Add more tests for other views as needed

    def test_show_photo_details_view(self):
        # Access the show_photo_details view for the test photo
        response = self.client.get(reverse('photo-details', args=[self.photo.pk]))

        # Check if the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Check if the photo is present in the context
        self.assertTrue('photo' in response.context)

        # Check if the CommentForm is present in the context
        self.assertTrue(isinstance(response.context['comment_form'], CommentForm))
