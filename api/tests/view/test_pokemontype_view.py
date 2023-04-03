from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import PokemonType
from api.serializers import PokemonTypeSerializer


class PokemonTypeListViewTests(APITestCase):
    def setUp(self):
        # Create test objects
        for i in range(20):
            PokemonType.objects.create(name=f"type{i}")

    def test_get_pokemon_type_list(self):
        """
        Tests the GET method, with pagination.
        """
        url = reverse("type-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test pagination
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIsNotNone(response.data["next"])

        # Test that the total count of objects in the database matches the count field in the response
        self.assertEqual(PokemonType.objects.count(), response.data["count"])

    def test_filter_pokemon_type_list(self):
        """
        Tests the SearchFilter to search for text in the PokemonType name field.
        """
        # Search for the first type
        url = reverse("type-list")
        response = self.client.get(url, {"search": "type0"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test that only one object is returned
        self.assertEqual(len(response.data["results"]), 1)

        # Test that the correct object is returned
        expected_result = PokemonTypeSerializer(PokemonType.objects.get(name="type0")).data
        self.assertEqual(response.data["results"][0], expected_result)


class PokemonTypeDetailTests(APITestCase):
    def setUp(self):
        self.type1 = PokemonType.objects.create(name="type 1")

    def test_retrieve_pokemon_type(self):
        """
        Tests the GET method to get a specific PokemonType by its id.
        """
        url = reverse("type-by-id", kwargs={"pk": self.type1.pk})
        response = self.client.get(url)
        type1_from_db = PokemonType.objects.get(id=self.type1.id)
        serializer = PokemonTypeSerializer(type1_from_db)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_pokemon_type(self):
        """
        Tests that a PokemonType can be updated by specifying its id.
        """
        url = reverse("type-by-id", kwargs={"pk": self.type1.pk})
        data = {"name": "new name"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.type1.refresh_from_db()
        self.assertEqual(self.type1.name, "new name")

    def test_delete_pokemon_type(self):
        """
        Tests that a PokemonType can be deleted by specifying its id.
        """
        url = reverse("type-by-id", kwargs={"pk": self.type1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(PokemonType.DoesNotExist):
            PokemonType.objects.get(id=self.type1.id)


class PokemonTypeFilterByNameTests(APITestCase):
    def setUp(self):
        self.type1 = PokemonType.objects.create(name="type 1")
        self.type2 = PokemonType.objects.create(name="type 2")
        self.url = reverse('type-filter-by-name', kwargs={'type_name': 'type 1'})

    def test_filter_by_name(self):
        """
        Tests that the view returns only the PokemonType with the given name.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = PokemonTypeSerializer([self.type1], many=True).data
        self.assertEqual(response.data['results'], serialized_data)

    def test_filter_by_nonexistent_name(self):
        """
        Tests that the view returns an empty list when a nonexistent name is given.
        """
        url = reverse('type-filter-by-name', kwargs={'type_name': 'nonexistent name'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
