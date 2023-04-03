from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import PokemonType
from api.serializers import PokemonTypeSerializer


class PokemonTypeSerializerTests(APITestCase):
	def setUp(self):
		# Valid values for every PokemonType field:
		self.type1 = PokemonType.objects.create(name="Pokemon Type 1")
		self.type2 = PokemonType.objects.create(name="Pokemon Type 2")
		self.type3 = PokemonType.objects.create(name="Pokemon Type 3")
		self.type4 = PokemonType.objects.create(name="Pokemon Type 4")
		self.valid_type = {
			"name": "Pokemon Type 5",
			"strong_vs": [self.type1.id],
			"weak_vs": [self.type2.id],
			"resistant_to": [self.type1.id, self.type3.id],
			"vulnerable_to": [self.type4.id]
		}

		# Invalid values for every PokemonType field:
		self.invalid_type = {
			"name": 123,
			"strong_vs": -1,
			"weak_vs": -1,
			"resistant_to": -1,
			"vulnerable_to": -1
		}

		# Valid values for every PokemonType field:
		self.updated_type = {
			"name": "Updated Pokemon Type 1",
			"strong_vs": [self.type2.id],
			"weak_vs": [self.type1.id],
			"resistant_to": [self.type2.id, self.type4.id],
			"vulnerable_to": [self.type3.id]
		}

	def test_pokemontype_serializer_valid(self):
		"""
		Tests that the serializer created with valid data is valid and
        that the PokemonType is saved correctly with no errors.
		"""
		serializer = PokemonTypeSerializer(data=self.valid_type)
		self.assertTrue(serializer.is_valid())
		pokemon_type = serializer.save()
		self.assertEqual(PokemonType.objects.count(), 5)
		self.assertEqual(pokemon_type.name, self.valid_type["name"])
		self.assertEqual(list(pokemon_type.strong_vs.all().values_list('id', flat=True)),
						 self.valid_type["strong_vs"])
		self.assertEqual(list(pokemon_type.weak_vs.all().values_list('id', flat=True)),
						 self.valid_type["weak_vs"])
		self.assertEqual(list(pokemon_type.resistant_to.all().values_list('id', flat=True)),
						 self.valid_type["resistant_to"])
		self.assertEqual(list(pokemon_type.vulnerable_to.all().values_list('id', flat=True)),
						 self.valid_type["vulnerable_to"])

	def test_pokemontype_serializer_invalid(self):
		"""
		Tests that the serializer created with invalid data is invalid and
		all invalid value fields are caught as errors.
		"""
		serializer = PokemonTypeSerializer(data=self.invalid_type)
		self.assertFalse(serializer.is_valid())
		self.assertEqual(set(serializer.errors.keys()), set(self.invalid_type.keys()))

	def test_pokemontype_serializer_create(self):
		"""
		Tests the instance is correctly saved to the database and the API endpoint
		can handle the creation of a new PokemonType instance with no errors.
		Verifies the response http status code is 201, which indicates that a new
		resource has been successfully created, and it also checks if the count of
		PokemonType objects has increased by one, which indicates that the new
		instance has been saved to the database.
		"""
		url = reverse("type-list")
		response = self.client.post(url, self.valid_type)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(PokemonType.objects.count(), 5)

	def test_pokemontype_serializer_update(self):
		"""
		Tests that an existing PokemonType instance can be updated by sending a valid
		PUT request to the API endpoint, verifying the response http status code is
		200, which indicates that the resource has been successfully updated, while
		the	updated fields match the updated data.
		"""
		type_to_update = PokemonType.objects.create(name="type to be updated")
		url = reverse("type-by-id", args=[type_to_update.id])
		response = self.client.put(url, self.updated_type)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		type_to_update.refresh_from_db()
		self.assertEqual(type_to_update.name, self.updated_type["name"])
		self.assertEqual(list(type_to_update.strong_vs.all().values_list('id', flat=True)),
						 self.updated_type["strong_vs"])
		self.assertEqual(list(type_to_update.weak_vs.all().values_list('id', flat=True)),
						 self.updated_type["weak_vs"])
		self.assertEqual(list(type_to_update.resistant_to.all().values_list('id', flat=True)),
						 self.updated_type["resistant_to"])
		self.assertEqual(list(type_to_update.vulnerable_to.all().values_list('id', flat=True)),
						 self.updated_type["vulnerable_to"])

	def test_pokemontype_serializer_delete(self):
		"""
		Tests that instance is correctly deleted from the database and the API endpoint
		can handle the deletion of a PokemonType instance with no errors.
		Verifies the response http status code is 404, which indicates a successful
		deletion, and finally checks that the instance is no longer present in the database.
		"""
		type_to_delete = PokemonType.objects.create(name="pokemon type to be deleted")
		url = reverse("type-by-id", args=[type_to_delete.id])
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(PokemonType.objects.count(), 4)
