from django.test import TestCase
from django.core.exceptions import ValidationError
from unittest.mock import Mock

from petstagram.photos.models import Photo
from petstagram.pets.models import Pet


# Arrange, Act, Assert
class PhotoTests(TestCase):
    VALID_PHOTO_DATA = {
        'photo': Mock(spec=['name', 'size']),
        'description': 'Test Description',
        'location': 'Test Location',
        'user': Mock(),
    }

    def _create_photo(self, data, **kwargs):
        pet = Pet.objects.create(name='Test Pet', owner=data['user'])
        photo_data = {
            **data,
            **kwargs,
            'user': pet.owner,
        }

        return Photo(**photo_data)

    def test_create__when_valid__expect_to_be_created(self):
        photo = self._create_photo(self.VALID_PHOTO_DATA)
        photo.full_clean()
        photo.save()

        self.assertIsNotNone(photo.pk)

    def test_create__when_description_has_1_more_than_valid_characters__expect_to_raise(self):
        invalid_data = {
            'description': 't' * Photo._meta.get_field('description').max_length + 't',
        }

        photo = self._create_photo(self.VALID_PHOTO_DATA, **invalid_data)

        with self.assertRaises(ValidationError):
            photo.full_clean()

    def test_create__when_location_is_none__expect_to_raise(self):
        invalid_data = {
            'location': None,
        }

        photo = self._create_photo(self.VALID_PHOTO_DATA, **invalid_data)

        with self.assertRaises(ValidationError):
            photo.full_clean()

    def test_create__when_location_starts_with_test___expect_to_raise(self):
        invalid_data = {
            'location': 'test_location',
        }

        photo = self._create_photo(self.VALID_PHOTO_DATA, **invalid_data)

        with self.assertRaises(ValidationError):
            photo.full_clean()

