from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Expansion
from datetime import date
from api.serializers import ExpansionSerializer


class ExpansionListTests(APITestCase):
	def setUp(self):
		self.expansion1 = Expansion.objects.create(
			name="expansion 1",
			series="series 1",
			release_date=date.today(),
		)
		self.expansion2 = Expansion.objects.create(
			name="expansion 2",
			series="series 2",
			release_date=date.today(),
		)

	def test_get_expansion_list(self):
		"""
		Tests that the GET request returns an HTTP_200_OK status code
		and that it returns the expected number of results.
		"""
		url = reverse("expansion-list")
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data["results"]), 2)

	def test_create_expansion(self):
		"""
		Tests that the POST request returns an HTTP_201_CREATED status
		code, that it creates a new Expansion object, and that it
		creates the object with the expected values.
		"""
		url = reverse("expansion-list")
		data = {"name": "expansion 3", "series": "series 3", "release_date": date.today()}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Expansion.objects.count(), 3)
		self.assertEqual(Expansion.objects.last().name, "expansion 3")



class ExpansionDetailTests(APITestCase):
	def setUp(self):
		self.expansion1 = Expansion.objects.create(
			name="expansion 1", series="series 1", release_date=date.today()
		)
		self.expansion2 = Expansion.objects.create(
			name="expansion 2", series="series 2", release_date=date.today()
		)

	def test_get_valid_expansion(self):
		"""
		Tests that a valid GET request to the view returns the correct data.
		"""
		url = reverse("expansion-by-id", kwargs={"pk": self.expansion1.pk})
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		expected_data = ExpansionSerializer(self.expansion1).data
		self.assertEqual(response.data, expected_data)

	def test_get_invalid_expansion(self):
		"""
		Tests that an invalid request returns a 404 status code.
		"""
		url = reverse("expansion-by-id", kwargs={"pk": 100})
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_update_valid_expansion(self):
		"""
		Tests that a valid PATCH request updates the correct object in the database.
		"""
		url = reverse("expansion-by-id", kwargs={"pk": self.expansion1.pk})
		data = {"name": "new expansion name"}
		response = self.client.patch(url, data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.expansion1.refresh_from_db()
		self.assertEqual(self.expansion1.name, data["name"])

	def test_delete_valid_expansion(self):
		"""
		Tests that a valid DELETE request deletes the correct object from the database.
		"""
		url = reverse("expansion-by-id", kwargs={"pk": self.expansion1.pk})
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Expansion.objects.filter(pk=self.expansion1.pk).exists())


class ExpansionFilterBySeriesTests(APITestCase):
	def setUp(self):
		self.expansion1 = Expansion.objects.create(name="expansion 1", series="series 1")
		self.expansion2 = Expansion.objects.create(name="expansion 2", series="series 2")
		self.expansion3 = Expansion.objects.create(name="expansion 3", series="series 1")
		self.url = reverse('expansion-list-by-series', kwargs={'series_name': 'series 1'})

	def test_expansions_are_filtered_by_series(self):
		"""
		Sends a GET request to the view URL, and asserts that the response status
		code is 200 and the response data matches the expected data.
		"""
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		expected_data = {
			'next': None,
			'previous': None,
			'count': Expansion.objects.filter(series__iexact="series 1").count(),
			'results': ExpansionSerializer(
				Expansion.objects.filter(series__iexact="series 1"),
				many=True
			).data
		}
		self.assertEqual(response.data, expected_data)

