from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Expansion
from api.serializers import ExpansionSerializer


class ExpansionSerializerTestCase(APITestCase):
	def setUp(self):
		# Valid values for every Expansion field:
		self.valid_expansion = {
			"name": "Expansion 1",
			"series": "Series 1",
			"cards": 200,
			"release_date": "2023-01-01",
			"promotional_set": False,
		}

		# Invalid values for every Expansion field:
		self.invalid_expansion = {
			"name": 123,
			"series": 321,
			"cards": "abc",
			"release_date": "invalid date",
			"promotional_set": "invalid_boolean",
		}

		# Valid values for every Expansion field:
		self.updated_expansion = {
			"name": "Updated Expansion 1",
			"series": "Series 2",
			"cards": 145,
			"release_date": "1999-02-10",
			"promotional_set": True,
		}

	def test_expansion_serializer_valid(self):
		"""
		Tests that the serializer created with valid data is valid and
		that the Expansion is saved correctly with no errors.
		"""
		serializer = ExpansionSerializer(data=self.valid_expansion)
		self.assertTrue(serializer.is_valid())
		expansion = serializer.save()
		self.assertEqual(Expansion.objects.count(), 1)
		self.assertEqual(expansion.name, self.valid_expansion["name"])
		self.assertEqual(expansion.series, self.valid_expansion["series"])
		self.assertEqual(expansion.cards, self.valid_expansion["cards"])
		self.assertEqual(str(expansion.release_date), self.valid_expansion["release_date"])
		self.assertEqual(expansion.promotional_set, self.valid_expansion["promotional_set"])

	def test_expansion_serializer_invalid(self):
		"""
		Tests that the serializer created with invalid data is invalid and
		all invalid value fields are caught as errors.
		"""
		serializer = ExpansionSerializer(data=self.invalid_expansion)
		self.assertFalse(serializer.is_valid())
		self.assertEqual(set(serializer.errors.keys()), set(self.invalid_expansion.keys()))

	def test_expansion_serializer_create(self):
		"""
		Tests the instance is correctly saved to the database and the API endpoint
		can handle the creation of a new Expansion instance with no errors.
		Verifies the response http status code is 201, which indicates that a new
		resource has been successfully created, and it also checks if the count of
		Expansion objects has increased by one, which indicates that the new
		instance has been saved to the database.
		"""
		url = reverse("expansion-list")
		response = self.client.post(url, self.valid_expansion)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Expansion.objects.count(), 1)

	def test_expansion_serializer_update(self):
		"""
		Tests that an existing Expansion instance can be updated by sending a valid
		PUT request to the API endpoint, verifying the response http status code is
		200, which indicates that the resource has been successfully updated, while
		the	updated fields match the updated data.
		"""
		expansion_to_update = Expansion.objects.create(name="expansion to be updated")
		url = reverse("expansion-by-id", args=[expansion_to_update.id])
		response = self.client.put(url, self.updated_expansion)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		expansion_to_update.refresh_from_db()
		self.assertEqual(expansion_to_update.name, self.updated_expansion["name"])
		self.assertEqual(expansion_to_update.series, self.updated_expansion["series"])
		self.assertEqual(expansion_to_update.cards, self.updated_expansion["cards"])
		self.assertEqual(str(expansion_to_update.release_date), self.updated_expansion["release_date"])
		self.assertEqual(expansion_to_update.promotional_set, self.updated_expansion["promotional_set"])

	def test_expansion_serializer_delete(self):
		"""
		Tests that instance is correctly deleted from the database and the API endpoint
		can handle the deletion of an Expansion instance with no errors.
		Verifies the response http status code is 404, which indicates a successful
		deletion, and finally checks that the instance is no longer present in the database.
		"""
		expansion_to_delete = Expansion.objects.create(name="expansion to be deleted")
		url = reverse("expansion-by-id", args=[expansion_to_delete.id])
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(Expansion.objects.count(), 0)
