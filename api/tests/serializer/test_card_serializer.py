import os
import tempfile
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from api.models import Expansion, PokemonType, Card
from api.serializers import CardSerializer
from io import BytesIO
from PIL import Image
from django.conf import settings
from decimal import Decimal
from django.urls import reverse
from rest_framework import status


class CardSerializerTestCase(APITestCase):
    def setUp(self):
        """
        Creates a temporary directory to store images.
        Creates test data: two dictionaries with valid values for fields in
        a Card object and one dictionary with invalid values.
        """
        # Temporary directory for images:
        super().setUp()
        self.temp_media = tempfile.TemporaryDirectory()
        settings.MEDIA_ROOT = self.temp_media.name
        print("Created temp directory for images:", self.temp_media.name)

        # Valid values for every Card field:
        self.valid_card = {
            "name": "card 1",
            "first_edition": True,
            "rarity": "common",
            "expansion": Expansion.objects.create(name="expansion 1").id,
            "type1": PokemonType.objects.create(name="type 1").id,
            "type2": PokemonType.objects.create(name="type 2").id,
            "hp": 100,
            "card_number": 1,
            "price": 9.99,
            "image": self.create_temp_image('image1.png')
        }

        # Invalid values for every Card field:
        self.invalid_card = {
            "name": 123,
            "rarity": "invalid rarity",
            "hp": 99,
            "expansion": -1,
            "type1": -1,
            "type2": -1,
            "card_number": "abc",
            "first_edition": "invalid_boolean",
            "price": "abc",
            "image": "invalid image",
        }

        # Valid values for every Card field:
        self.updated_card = {
            "name": "Updated Card 1",
            "rarity": "common",
            "hp": 50,
            "expansion": Expansion.objects.create(name="updated expansion").id,
            "type1": PokemonType.objects.create(name="updated type 1").id,
            "type2": PokemonType.objects.create(name="updated type 2").id,
            "card_number": 23,
            "first_edition": False,
            "price": 19.23,
            "image": self.create_temp_image('image2.png')
        }

    def create_temp_image(self, filename):
        """
        Creates a temporary image to be used in tests.
        """
        img_data = BytesIO()
        img = Image.new("RGB", (100, 100))
        img.save(img_data, format="PNG")
        img_data.seek(0)
        return SimpleUploadedFile(filename, img_data.getvalue())

    def test_card_serializer_valid(self):
        """
        Tests that the serializer created with valid data is valid and
        that the Card is saved correctly with no errors.
        """
        serializer = CardSerializer(data=self.valid_card)
        self.assertTrue(serializer.is_valid())
        card = serializer.save()
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(card.name, self.valid_card["name"])
        self.assertEqual(card.first_edition, self.valid_card["first_edition"])
        self.assertEqual(card.rarity, self.valid_card["rarity"])
        self.assertEqual(card.expansion.id, self.valid_card["expansion"])
        self.assertEqual(card.type1.id, self.valid_card["type1"])
        self.assertEqual(card.type2.id, self.valid_card["type2"])
        self.assertEqual(card.hp, self.valid_card["hp"])
        self.assertEqual(card.card_number, self.valid_card["card_number"])
        self.assertEqual(card.price, Decimal(str(self.valid_card["price"])))
        self.assertTrue(card.image, self.valid_card["image"])

    def test_card_serializer_invalid(self):
        """
		Tests that the serializer created with invalid data is invalid and
		all invalid value fields are caught as errors.
		"""
        serializer = CardSerializer(data=self.invalid_card)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(self.invalid_card.keys()))

    def test_card_serializer_create(self):
        """
        Tests the instance is correctly saved to the database and the API endpoint
        can handle the creation of a new Card instance with no errors.
        Verifies the response http status code is 201, which indicates that a new
        resource has been successfully created, and it also checks if the count of
        Card objects has increased by one, which indicates that the new
        instance has been saved to the database.
        """
        url = reverse("card-list")
        response = self.client.post(url, self.valid_card)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Card.objects.count(), 1)

    def test_card_serializer_update(self):
        """
		Tests that a Card can be updated with no errors.
		"""
        card_to_update = Card.objects.create(name="card to be updated")
        url = reverse("card-by-id", args=[card_to_update.id])
        response = self.client.put(url, self.updated_card)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        card_to_update.refresh_from_db()
        self.assertEqual(card_to_update.name, self.updated_card["name"])
        self.assertEqual(card_to_update.rarity, self.updated_card["rarity"])
        self.assertEqual(card_to_update.hp, self.updated_card["hp"])
        self.assertEqual(card_to_update.expansion_id, self.updated_card["expansion"])
        self.assertEqual(card_to_update.type1_id, self.updated_card["type1"])
        self.assertEqual(card_to_update.type2_id, self.updated_card["type2"])
        self.assertEqual(card_to_update.card_number, self.updated_card["card_number"])
        self.assertEqual(card_to_update.first_edition, self.updated_card["first_edition"])
        self.assertEqual(card_to_update.price, Decimal(str(self.updated_card["price"])))
        self.assertEqual(os.path.basename(card_to_update.image.name), self.updated_card["image"].name)

    def test_card_serializer_delete(self):
        """
        Tests that instance is correctly deleted from the database and the API endpoint
        can handle the deletion of a Card instance with no errors.
        Verifies the response http status code is 204, which indicates a successful
        deletion, and finally checks that the instance is no longer present in the database.
        """
        card_to_delete = Card.objects.create(name="card to be deleted")
        url = reverse("card-by-id", args=[card_to_delete.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Card.objects.count(), 0)
